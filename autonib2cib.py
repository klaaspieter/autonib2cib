#!/usr/bin/env python
# encoding: utf-8

# Created by Klaas Pieter Annema.
# 
# Copyright (c) 2011 Klaas Pieter Annema
# 
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import sys
import os
import commands
import hashlib
import baker
import logging
from colorlogger import *

from pyfsevents import registerpath, listen

# @baker.command
# def version():
# 	print '0.1'

@baker.command(default=True, shortopts={"versbose":"v"}, params={"verbose": "Spew lots"})
def monitor(path, verbose=False):

	logger = logging.getLogger('')

	handler = logging.StreamHandler()
	handler.setLevel(logging.DEBUG)
	handler.setFormatter(ColorFormatter())
	logger.addHandler(handler)

	if verbose:
		logger.setLevel(logging.DEBUG)
	else:
		logger.setLevel(logging.INFO)

	path = os.path.abspath(path)
	
	if not os.path.isdir(path):
		logging.error('Not a directory: %s' % path)
		return
	
	# We'll get a callback that the monitored directory changed. To determine
	# which file was changed we keep a checksum and compare it when the directory
	# change event is received
	checksums = {}

	files = os.listdir(path)
	for filename in files:
		
		# Only monitor files with the .xib extension
		if not isXibFile(filename):
			continue

		checksums[filename] = hashfile(os.path.join(path, filename))
	
	def rebuild(path, recursive):

		for filename in os.listdir(path):

			if not isXibFile(filename):
				continue

			checksum = hashfile(os.path.join(path, filename))
			cachedChecksum = checksums.get(filename, None)
			
			if cachedChecksum == checksum:
				continue

			# Cache the new checksum because it was changed
			checksums[filename] = checksum

			# nib2cib doesn't support absolute paths for the resource path
			# so we use the relative path for the -R option
			command = 'nib2cib %s -R %s' % (os.path.join(path, filename), os.path.relpath(path))
			
			logging.info(command)
			
			output = commands.getstatusoutput(command)[1]
			
			# Unfortunately nib2cib doesn't return proper status so we can't log an error
			# if it exited with a non zero exit status
			# If you need to see errors, use verbose mode
			if not ' '.join(output.split()):
				logging.debug(' '.join(output.split()))
			else:
				logging.debug('No output')

	registerpath(path, rebuild)

	listen()
	
def isXibFile(filename):
	return os.path.splitext(filename)[1] == '.xib'

def hashfile(path):
	return hashlib.md5(file(path, 'rb').read()).digest()

# Prevent CTRL+C from logging a stacktrace
try:
	baker.run()
except KeyboardInterrupt:
	sys.exit(0)
