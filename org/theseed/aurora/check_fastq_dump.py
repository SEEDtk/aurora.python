#! /usr/bin/env python3
# check_fastq_dump.py - Check the integrity of FASTQ dump files.
'''
This script looks at a FASTQ dump directory created by genome.download and deletes the incomplete dumps.
An incomplete dump is one that has no summary.txt file.

Usage:
    python check_fastq_dump.py <dump_directory>
'''
import sys
import argparse
import os
import shutil


def main():
    parser = argparse.ArgumentParser(description="Check the integrity of FASTQ dump files.")
    parser.add_argument("dump_directory", type=str, help="Directory containing FASTQ dumps")
    args = parser.parse_args()
    indir = os.path.abspath(args.dump_directory)
    if not os.path.isdir(indir):
        sys.stderr.write(f"Error: {indir} is not a valid directory.\n")
        return 1

    for root, dirs, files in os.walk(indir):
        # Only proceed if we are NOT the top-level directory.
        if indir != root:
            if not ("summary.txt" in files):
                # This is an incomplete dump.  We will delete it.
                sys.stderr.write(f"Deleting incomplete dump: {root}\n")
                shutil.rmtree(root)
    return 0

if __name__ == "__main__":
    sys.exit(main())
    