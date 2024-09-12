#!/usr/local/bin/python2.7
# encoding: utf-8
'''
org.theseed.aurora.md5Check -- isolate duplicate MD5s in a sorted genome list

org.theseed.aurora.md5Check is a command to mark duplicate records in a sorted genome list


@author:     Bruce Parrello

@copyright:  2024 University of Chicago. All rights reserved.

@contact:    brucep.mobile@gmail.com
'''
import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2024-09-12'
__updated__ = '2024-09-12'

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

def parseRecord(line):
    ''' Return the fields of the record. '''
    recordString = line.strip("\n")
    retVal = recordString.split("\t")
    return retVal


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

  Created by user_name on %s.
  Copyright 2024 organization_name. All rights reserved.

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
        parser.add_argument(dest="inFile", help="name of input file", metavar="inFile")

        # Process arguments
        args = parser.parse_args()

        inFile = args.inFile
        verbose = args.verbose

        if verbose > 0:
            print("Verbose mode on")
        dupCount = 0
        with open(inFile) as inStream:
            # Read and echo the header
            line1 = inStream.readline()
            header = line1.rstrip("\n") + "\tdup";
            print(header)
            oldMd5 = "x"
            for line in inStream:
                fields = parseRecord(line)
                md5 = fields[-1]
                if md5 == oldMd5:
                    dup = "Y"
                    dupCount += 1
                else:
                    dup = ""
                    oldMd5 = md5
                lineOut = "\t".join(fields) + "\t" + dup
                print(lineOut)
        sys.stderr.write(f"{dupCount} duplicates.\n")
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
        #sys.argv.append("-h")
        sys.argv.append("-v")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'org.theseed.aurora.md5Check_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())