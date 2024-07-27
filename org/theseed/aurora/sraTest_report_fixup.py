#!/usr/local/bin/python2.7
# encoding: utf-8
'''
org.theseed.aurora.sraTest_report_fixup -- fix up SRA test reports

org.theseed.aurora.sraTest_report_fixup is a command that created derived reports from the basic sraTest report cluster


@author:     Bruce Parrello

@copyright:  2024 Fellowship for Interpretation of Genomes. All rights reserved.


@contact:    brucep.mobile@gmail.com
@deffield    updated: Updated
'''

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2024-07-26'
__updated__ = '2024-07-26'

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

def getRecord(inIter):
    ''' Return the fields of the next record. '''
    recordString = next(inIter)
    recordString = recordString.strip("\n")
    retVal = recordString.split("\t")
    return retVal

def getType(fields):
    ''' Remove the record type from the fields and return it '''
    retVal = fields.pop(2)
    return retVal

def writeLine(fields, outStream):
    ''' Write a line of text '''
    line = "\t".join(fields) + "\n"
    outStream.write(line)

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
        parser.add_argument(dest="path", help="path to folder with source files [default: %(default)s]", metavar="path")
        parser.add_argument(dest="prefix", help="file prefix for type of reports", metavar="prefix")

        # Process arguments
        args = parser.parse_args()

        path = args.path
        prefix = args.prefix
        verbose = args.verbose

        if verbose > 0:
            print("Verbose mode on")

        # This section processes the roles report.  In this report, each sample has two lines of data-- one for
        # good hits and one for bad hits.  We convert the two lines to a single line containing the % of hits
        # that were bad.
        roleFile = os.path.join(path, prefix + ".roles.tbl")
        outFile = os.path.join(path, prefix + ".rolePct.tbl")
        with open(roleFile, 'r') as roleStream, open(outFile, 'w') as outStream:
            lines = roleStream.readlines()
            inIter = iter(lines)
            # Process the header.  We remove the type column and write it out.
            header = getRecord(inIter)
            recType = getType(header)
            writeLine(header, outStream)
            nWidth = len(header)
            # Now we need to loop through the data.  We store each line in a dictionary keyed by the first
            # two columns.
            goodLines = {}
            badLines = {}
            keyList = []
            n = len(lines)
            lastKey = ""
            for i in range(1, n):
                fields = getRecord(inIter)
                recType = getType(fields)
                print(f"Processing {recType} record {i}.")
                key = fields[0] + "\t" + fields[1]
                if recType == "good":
                    goodLines[key] = fields
                else:
                    badLines[key] = fields
                if key != lastKey:
                    keyList.add(key)
                    lastKey = key
            # Now we loop through the key list, extracting the good and bad lines and
            # combining them.
            print("Writing output.")
            for key in keyList:
                outList = [key]
                if not (key in badLines):
                    # Here we are all good.
                    for i in range(2, nWidth):
                        outList.append("0.0")
                elif not (key in goodLines):
                    # Here we are all bad.
                    for i in range(2, nWidth):
                        outList.append("1.0")
                else:
                    goodLine = goodLines[key]
                    badLine = badLines[key]
                    for i in range(2, nWidth):
                        bad = float(badLine[i])
                        good = float(goodLine[i])
                        if bad == 0:
                            outList.append("0.0")
                        else:
                            outList.append(str(bad / (bad + good)))
                writeLine(outList, outStream)

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
        profile_filename = 'org.theseed.aurora.sraTest_report_fixup_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
