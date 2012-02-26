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

import time

from tests.gui import TestFinished
from tests.gui.multiplayer import mp_player, MPTest


@mp_player
def player1(gui):
	yield
	while not gui.find(name='gold_available'):
		yield
	yield TestFinished


@mp_player
def player2(gui):
	yield
	while not gui.find(name='gold_available'):
		yield
	yield TestFinished


def test():
	failure = False

	p1 = MPTest(player1, master=True)
	p2 = MPTest(player2)

	# give p1 some time to start the game
	p1.start()
	time.sleep(5)

	p2.start()

	# let both players run for a while
	time.sleep(10)

	# if everything went well, they should have stopped
	if not p1.stopped() or not p2.stopped():
		assert False

test.gui = True
