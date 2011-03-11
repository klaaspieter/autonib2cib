#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import commands
import hashlib
import getopt

from pyfsevents import registerpath, listen

def usage():
	return 'usage: %s [PATH]' % os.path.basename(__file__)

def main(argv=None):
	if argv is None:
		argv = sys.argv

	if len(argv) != 2:
		print usage()
		return 1

	path = os.path.normcase(os.path.abspath(argv[1]))

	if not os.path.isdir(path):
		print 'Not a directory: %s' % path
		print usage()
		return 1

	checksums = {}
	files = os.listdir(path)

	for filename in files:

		if os.path.splitext(filename)[1] != '.xib':
			continue

		xibfile = file(os.path.join(path, filename), 'rb')

		checksums[filename] = hashlib.md5(xibfile.read()).digest()

	def rebuild(path, recursive):
		
		for filename in os.listdir(path):

			if os.path.splitext(filename)[1] != '.xib':
				continue

			xibfile = file(os.path.join(path, filename), 'rb')
			checksum = hashlib.md5(xibfile.read()).digest();

			cachedChecksum = checksums.get(filename, None)
			if cachedChecksum == None or cachedChecksum == checksum:
				continue

			checksums[filename] = checksum

			command = 'nib2cib %s -R %s' % (os.path.join(path, filename), path)

			print command
			output = commands.getstatusoutput(command)

			assert output[0] == 0, output

	registerpath(path, rebuild)

	print 'Listening for changes at %s' % path

	listen()

if __name__ == "__main__":
	sys.exit(main())