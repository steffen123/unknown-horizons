# -*- coding: utf-8 -*-
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

from horizons.gui.tabs import OverviewTab
from horizons.component.storagecomponent import StorageComponent
from horizons.component.selectablecomponent import SelectableComponent

class GroundUnitOverviewTab(OverviewTab):
	has_stance = True
	def __init__(self, instance):
		super(GroundUnitOverviewTab, self).__init__(
			widget = 'overview_groundunit.xml',
			instance = instance)
		self.helptext = _("Unit overview")
		health_widget = self.widget.findChild(name='health')
		health_widget.init(self.instance)
		self.add_remove_listener(health_widget.remove)
		weapon_storage_widget = self.widget.findChild(name='weapon_storage')
		weapon_storage_widget.init(self.instance)
		self.add_remove_listener(weapon_storage_widget.remove)

class EnemyGroundUnitOverviewTab(OverviewTab):
	def  __init__(self, instance):
		super(EnemyGroundUnitOverviewTab, self).__init__(
			widget = 'overview_enemyunit.xml',
			instance = instance)