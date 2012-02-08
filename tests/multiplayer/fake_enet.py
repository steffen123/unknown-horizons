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

"""Provides a fake enet module.

Basically replaces the network-based transport with a list of queues in the same
process. Hopefully makes it easy to verify that in-game actions produce the correct
packets."""

from collections import deque, defaultdict

import pickle
import logging

import gevent
import enet_original
from enet_original import EVENT_TYPE_CONNECT, EVENT_TYPE_NONE, EVENT_TYPE_DISCONNECT, EVENT_TYPE_RECEIVE


log = logging.getLogger(__name__)


# Global event queue
events = defaultdict(deque)

def add_event(address, type, peer, data=None):
	event = Event(type, peer, data)
	events[str(address)].append(event)


class Address(enet_original.Address):
	"""Need to redefine Address, otherwise isinstance checks will fail."""
	pass


class Peer(object):

	def __init__(self, origin, target):
		self.address = target
		self.origin = origin
		self.data = None

	def send(self, channel, packet):
		log.debug('Peer.send %s to %s' % (pickle.loads(packet.data), self.address))

		add_event(self.address, EVENT_TYPE_RECEIVE, self, packet)

	def reset(self):
		log.debug('Peer.reset')

	def __repr__(self):
		return '<Peer %s>' % self.address


class Event(object):

	def __init__(self, type, peer, data=None):
		log.debug('Event.new %s %s %s' % (type, peer, data))

		self.type = type
		self.peer = peer 
		self.data = data
		self.packet = data

	def __repr__(self):
		return '<Event type: %d peer: %s>' % (self.type, self.peer)


class Host(object):

	def __init__(self, address, *args, **kwargs):
		log.debug('Host.new %s %s %s' % (address, args, kwargs))

		self.address = address

	def service(self, *args):
		log.debug('Host.service %s %s' % (self.address, args))

		my_events = events[str(self.address)]
		while not my_events:
			gevent.sleep(0)

		event = my_events.popleft()
		# Switch source and destination address
		event.peer.origin, event.peer.address = event.peer.address, event.peer.origin
		return event

	def connect(self, address, channel_count, data):
		log.debug('Host.connect %s %s' % (address, data))

		remote_peer = Peer(address, self.address)

		add_event(address, EVENT_TYPE_CONNECT, remote_peer, data)
		add_event(self.address, EVENT_TYPE_CONNECT, remote_peer)

		return remote_peer

	def flush(self):
		pass
