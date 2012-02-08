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
import subprocess
import sys

from horizons.constants import VERSION
from horizons.ext.dummy import Dummy
from horizons.extscheduler import ExtScheduler
from horizons.network import find_enet_module
from horizons.network.client import Client
from horizons.network.networkinterface import NetworkInterface


def setup_package():
	ExtScheduler.create_instance(Dummy())
	enet = find_enet_module()

	# make enet.Host co-routine friendly
	class Host(enet.Host):
		def service(self, *args, **kwargs):
			gevent.sleep(0)
			return super(Host, self).service(*args, **kwargs)

	enet.Host = Host


def _create_interface(name, address):
	def setup_client(self):
		self._client = Client(name, VERSION.RELEASE_VERSION, ['127.0.0.1', 2002], address)
	NetworkInterface._NetworkInterface__setup_client = setup_client

	NetworkInterface.destroy_instance()
	NetworkInterface.create_instance()
	return NetworkInterface()


def run_server():
	try:
		p = subprocess.Popen([sys.executable, 'server.py', '-h', '127.0.0.1'])
		while True:
			gevent.sleep(0)
			p.poll()
			if p.returncode:
				break
	finally:
		p.terminate()


def new_client(name, address):
	p = _create_interface(name, address)
	p.connect()
	return p


def test_example():
	def client(server):
		p1 = new_client('Dagobert', ['127.0.0.1', 3000])
		assert p1.get_active_games() == []
		p1.change_name('Duffy', save=False)
		game = p1.creategame('development', 2)
		assert game.get_player_count() == 1

		p2 = new_client('Donald', ['127.0.0.1', 3001])
		assert len(p2.get_active_games()) == 1
		p2.joingame(game.uuid)

		p1.disconnect()
		p2.disconnect()
		server.kill()

	s = gevent.spawn(run_server)
	c = gevent.spawn_later(3, client, s) # wait for server to be ready
	gevent.joinall([c, s])


"""
def test_lobby():
	def client(server):
		p1 = new_client('P1', ['127.0.0.1', 3000])
		p2 = new_client('P2', ['127.0.0.1', 3001])

		game = p1.creategame('development', 2)
		assert p1._client.game

		called = False
		def prepare(game):
			called = True
			print 'Game is prepared', game

		p1.register_game_prepare_callback(prepare)
		p2.register_game_prepare_callback(prepare)
		p2.joingame(game.uuid)

		while not called:
			gevent.sleep(0)

		p1.disconnect()
		gevent.sleep(0)
		p2.disconnect()
		gevent.sleep(0)
		server.kill()

	s = gevent.spawn(run_server)
	c = gevent.spawn_later(3, client, s) # wait for server to be ready
	gevent.joinall([c, s])
"""
