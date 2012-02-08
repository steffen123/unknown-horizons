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

from tests.gui import gui_test


# The `gui_test` decorator is needed to identify gui tests. You can use it
# without argument, but is has to be `@gui_test()` (notice the parantheses).
#
# It accepts either one of these arguments:
#
# 	use_dev_map=True		- Game launches with --start-dev-map (no main menu)
# 	use_fixture='name'		- Game launches with --load-map=tests/gui/ingame/fixtures/name.sqlite
# 	ai_players=1			- Game launches with --ai-players=1
# 	timeout=3				- Game will be killed after 3 seconds
#
@gui_test(timeout=60)
def test_example(gui):
	"""
	Documented example test.

	Every gui test has to accept one argument, an instance of `tests.gui.GuiHelper`.
	"""
	gui.disable_autoscroll()

	# Main menu
	main_menu = gui.find(name='menu')
	gui.trigger(main_menu, 'startSingle/action/default')

	# Single-player menu
	assert len(gui.active_widgets) == 1
	singleplayer_menu = gui.active_widgets[0]
	gui.trigger(singleplayer_menu, 'okay/action/default') # start a game

	# Hopefully we're ingame now
	assert len(gui.active_widgets) == 3
	gold_label = gui.find(name='gold_available')
	assert gold_label.text == '30000'

	# All commands above run sequentially, neither the engine nor the timer
	# will be run. If you need the game to run for some time (or have to wait for
	# something to happen), use `gui.run`.
	# Despite the wording, the 2 seconds will elapse once the game simulation ran 2
	# seconds. If the game is paused, this will run longer.
	gui.run(seconds=2)

	"""
	while not condition:
		gui.run() # run the game for one tick
	"""

	# When you call `gui.run` the engine is allowed to run, therefore updating the display.
	# You can also interact with the game as normal, but please don't mess with the test. :)
	#
	# TIP: You can watch the test in slow-motion if you insert these waits between
	# interactions.

	# Open game menu
	gui.trigger('mainhud', 'gameMenuButton/action/default')

	# gui.trigger accepts both a string (container name), or a object returned by gui.find

	# Cancel current game
	def dialog():
		gui.trigger('popup_window', 'okButton/action/__execute__')

	# Dialog handling has to be done by a separate function.
	with gui.handler(dialog):
		gui.trigger('menu', 'quit/action/default')

	# Code execution will continue here once `dialog` has ended.

	# Back at the main menu
	assert gui.find(name='menu')

	# By default, the game will end once the test function returns.
	# If you return something different from None, the game continues to run:
	# return 1
