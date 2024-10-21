#!/usr/local/bin/python2.7
# encoding: utf-8
'''
org.theseed.aurora.response_clean -- Remove response headers from SOLR dumps

org.theseed.aurora.response_clean is a simple command that processes a SOLR dump and removes response headers from the JSON

It defines classes_and_methods

@author:     Bruce Parrello

@copyright:  2024 University of Chicago. All rights reserved.

@contact:    brucep.mobile@gmail.com
'''

import sys
import os
import json

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from pathlib import Path

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
        parser.add_argument(dest="outpath", help="path to folder to contain output files", metavar="outpath")
        parser.add_argument(dest="paths", help="paths to folder(s) with source file(s) [default: %(default)s]", metavar="path", nargs='+')

        # Process arguments
        args = parser.parse_args()

        outpath = args.outpath
        paths = args.paths
        verbose = args.verbose

        if verbose > 0:
            print("Verbose mode on")

        # Set up some counters.
        dirsIn = 0
        filesIn = 0
        copied = 0
        cleaned = 0
        singleIn = 0
        emptyIn = 0
        # Loop through the input directories.
        for inpath in paths:
            # Get the subdirectories of this one.
            subdirs = [f.name for f in os.scandir(inpath) if f.is_dir()]
            for subdir in subdirs:
                dirsIn += 1
                # Compute the input and output paths for this subdirectory.
                dirpath = inpath + "/" + subdir
                outdir = outpath + "/" + subdir
                # Insure the output directory exists.
                Path(outdir).mkdir(parents=True, exist_ok=True)
                # Get all the files in the input subdirectory.
                dirfiles = [f.name for f in os.scandir(dirpath) if not f.is_dir()]
                for jsonfile in dirfiles:
                    # Only proceed if this is a JSON file.
                    if jsonfile.endswith(".json"):
                        filesIn += 1
                        # Get the input and output file names.
                        jsonpath = dirpath + "/" + jsonfile
                        jsonout = outdir + "/" + jsonfile
                        print(f"Copying {jsonpath} to {jsonout}.")
                        # Read the dump as a JSON object.
                        with open(jsonpath, "r") as f:
                            json_str = f.read()
                        if json_str == "":
                            emptyIn +=1
                            with open(jsonout, "w") as f:
                                f.write("[]")
                        else:
                            json_obj = json.loads(json_str)
                            if isinstance(json_obj, list):
                                # A list requires no alteration.
                                doc_obj = json_obj
                                copied += 1
                            elif isinstance(json_obj, dict):
                                # Here we have a dictionary, which means we probably
                                # have a response header. If we have a response header, get
                                # the document element and return it. Otherwise, but the
                                # dictionary object in a list.
                                if "response" in json_obj:
                                    doc_obj = json_obj["response"]["docs"]
                                    cleaned += 1
                                else:
                                    doc_obj = [json_obj]
                                    singleIn += 1
                            else:
                                # Here we have a scalar. Return an empty list.
                                doc_obj = []
                                emptyIn += 1
                            # Write the output file.
                            with open(jsonout, "w") as f:
                                f.write(json.dumps(doc_obj))
        print(f"{dirsIn} directories, {filesIn} files, {cleaned} cleaned, {copied} copied, {emptyIn} empty, {singleIn} singletons.")
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
