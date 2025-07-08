#! /usr/bin/env python3
# combine_text_files.py - Combine multiple text files into one.
'''
This script concatenates multiple text files into a single output file. The default action
is to create the output on the standard output, but an output file can be specified with the -o option.
The input files are specified as positional arguments.

Usage:
    python combine_text_files.py -o <output_file> <input_file1> <input_file2> ... <input_fileN>
'''
import sys
import argparse
import os

def copy_file(fname, outfile):
    sys.stderr.write(f"Copying {fname} to output.\n")
    if not os.path.isfile(fname):
        sys.stderr.write(f"Error: {fname} is not a valid file.\n")
        return
    with open(fname) as infile:
        outfile.write(infile.read())

def main():
    parser = argparse.ArgumentParser(description="Combine multiple text files into one.")
    parser.add_argument("-o", "--output", type=str, help="Output file name")
    parser.add_argument("inputs", nargs="+", help="Input files to combine")
    args = parser.parse_args()

    if args.output:
        outfile = open(args.output, "w")
    else:
        outfile = sys.stdout
    for fname in args.inputs:
        if os.path.isdir(fname):
            sys.stderr.write(f"Processing directory: {fname}\n")
            for root, dirs, files in os.walk(fname):
                for f in files:
                    copy_file(os.path.join(root, f), outfile)
        else:
            copy_file(fname, outfile)
    if args.output:
        outfile.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())
    