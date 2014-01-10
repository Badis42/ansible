# (c) 2012-2014, Michael DeHaan <michael.dehaan@gmail.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

class HostVarsProxy(dict):
    ''' A special view of setup_cache that adds values from the inventory when needed. '''

    def __init__(self, setup_cache, inventory):
        self.setup_cache = setup_cache
        self.inventory = inventory
        self.lookup = dict()
        self.update(setup_cache)

    def __getitem__(self, host):
        if host not in self.lookup:
            result = self.inventory.get_variables(host)
            result.update(self.setup_cache.get(host, {}))
            self.lookup[host] = result
        return self.lookup[host]


