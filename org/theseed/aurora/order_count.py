#!/usr/local/bin/python2.7
# encoding: utf-8
'''
org.theseed.aurora.order_count -- Count species within order in SOLR dumps

org.theseed.aurora.type_count is a simple command that processes a SOLR dump and counts the species in each order

@author:     Bruce Parrello

@copyright:  2024 University of Chicago. All rights reserved.

@contact:    brucep.mobile@gmail.com
'''

import sys
import os
import json

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2024-10-21'
__updated__ = '2024-10-21'

DEBUG = 1
TESTRUN = 0
PROFILE = 0

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by Bruce Parrello on %s.
  Copyright 2024 University of Chicago. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument(dest="paths", help="paths to folder(s) with source file(s) [default: %(default)s]", metavar="path", nargs='+')

        # Process arguments
        args = parser.parse_args()

        paths = args.paths
        verbose = args.verbose

        if verbose > 0:
            print("Verbose mode on")

        # Set up some counters.
        dirsIn = 0
        order_species_counts = {}
        # Loop through the input directories.
        for inpath in paths:
            # Get the subdirectories of this one.
            subdirs = [f.name for f in os.scandir(inpath) if f.is_dir()]
            for subdir in subdirs:
                dirsIn += 1
                # Compute the input and output paths for this subdirectory.
                dirpath = inpath + "/" + subdir
                # Get the genome_feature.json file in the input subdirectory.
                fidfile = dirpath + "/genome.json"
                # Read the feature dump as a JSON object.
                with open(fidfile, "r") as f:
                    json_str = f.read()
                    json_obj = json.loads(json_str)
                    genome = json_obj[0]
                    order = genome["order"]
                    species = genome["species"]
                    if not (order in order_species_counts):
                        order_species_counts[order] = {};
                    species_map = order_species_counts[order]
                    if not (species in species_map):
                        species_map[species] = 1
                    else:
                        species_map[species] += 1
        print(f"{dirsIn} directories processed.")
        print("")
        for order in order_species_counts:
            orderStr = order.ljust(15, " ")
            species_map = order_species_counts[order]
            for species in species_map:
                count = str(species_map[species]).rjust(15, " ")
                speciesStr = species.ljust(15, " ")
                print(f"{orderStr} {speciesStr} {count}")
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-v")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'org.theseed.aurora.response_clean_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
