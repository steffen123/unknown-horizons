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

import gevent

from horizons.constants import VERSION
from horizons.ext.dummy import Dummy
from horizons.extscheduler import ExtScheduler
from horizons.network.client import Client
from horizons.network.networkinterface import NetworkInterface
from horizons.network.server import Server


def setup_package():
	ExtScheduler.create_instance(Dummy())


def _create_interface(name, address):
	def setup_client(self):
		self._client = Client(name, VERSION.RELEASE_VERSION, ['8.8.8.8', 88], address)
	NetworkInterface._NetworkInterface__setup_client = setup_client

	NetworkInterface.destroy_instance()
	NetworkInterface.create_instance()
	return NetworkInterface()


def test_example():
	def server():
		server = Server('8.8.8.8', 88, None)
		server.run()

	def client():
		p1 = _create_interface('Dagobert', ['1.1.1.1', 11])
		p1.connect()
		assert p1.get_active_games() == []
		p1.change_name('Duffy', save=False)
		game = p1.creategame('development', 2)
		assert game.get_player_count() == 1

		p2 = _create_interface('Donald', ['2.2.2.2', 22])
		p2.connect()
		assert len(p2.get_active_games()) == 1
		p2.joingame(game.uuid)

	s = gevent.spawn(server)
	c = gevent.spawn(client)
	gevent.joinall([s, c])
