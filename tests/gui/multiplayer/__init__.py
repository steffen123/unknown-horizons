# ###################################################
# Copyright (C) 2012 The Unknown Horizons Team
# team@unknown-horizons.org
# This file is part of Unknown Horizons.
#
# Unknown Horizons is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# ###################################################

import os
import subprocess
import sys


def mp_player(func):
	"""Hack to use the gui test runner"""
	func.__original__ = func
	func.__test__ = False
	return func
mp_player.__test__ = False


class MPTest(object):
	""" """
	def __init__(self, test, master=False):
		self.test = test
		self.master = master

	def start(self):
		""" """
		role = self.master and '--create-mp-game' or '--join-mp-game'
		test_name = '%s.%s' % (self.test.__module__, self.test.__name__)
		args = [sys.executable, 'run_uh.py', '--gui-test', test_name, role]

		env = os.environ.copy()
		env['FAIL_FAST'] = '1'

		self.proc = subprocess.Popen(args, env=env)

	def stopped(self):
		self.proc.poll()
		if self.proc.returncode is None:
			self.proc.terminate()	
			return False
		return True
