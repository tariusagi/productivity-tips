#!/usr/bin/env python3
"""A basic Python 3 program with simple command line argument handling"""
VERSION = "0.1"

# Module imports.
import os
import sys
import getopt

# File name and path to this script.
FILE = os.path.basename(__file__)
PATH=os.path.dirname(os.path.abspath(__file__))

# Program usage.
USAGE = f"""\
{FILE} version {VERSION} from {PATH}
Syntax: {FILE} [OPTION] TEXT
A basic Python program that say repeat anything given to it in TEXT.

OPTION:
  -h, --help                  Print this usage.
  -n, --name=NAME             Set the name to say hi to.
"""

def main():
	"""Main function of this program."""
	# Default arguments.
	name = "Stranger"
	# If no argument was provided, print the usage and exit.
	if len(sys.argv) == 1:
		print(USAGE)
		sys.exit(0)
	# Handle commandline arguments.
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'hn:', ["help", "name="])
	except getopt.error as err:
		print(f'ERROR: {str(err)}. Use "-h" for usage.', file = sys.stderr)
		sys.exit(1)
	for o, v in opts:
		if o in ('-h', '--help'):
			print(USAGE)
			sys.exit(0)
		elif o in ('-n', '--name'):
			name = v
		else:
			print('ERROR: Unknown option. Use "-h" for usage.', file = sys.stderr);
			sys.exit(2)
	# Join all remaining arguments into a string.
	text = ' '.join(args)
	if len(text):
		print("Hello %s, did you say %s?" % (name, text))
	else:
		print("Hello %s, you are quiet! Are you OK?" % name)

# Entry.
if __name__ == '__main__':
	main()

