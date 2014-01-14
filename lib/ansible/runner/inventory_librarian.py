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

from ansible import utils

class InventoryLibrarian(object):
    ''' 
    The inventory librarian responds to requests to access variables about hosts or groups by providing
    data on them.  Certain special logic may be required for special variables, where something may
    default to a parameter passed in to runner if an inventory variable is not set.

    For those remembering the old code, the purpose of InventoryLibrarian is to eliminate the need (or rather to construct)
    things like the 'inject' dictionary which is input into various templating calls throughout Ansible, as well as to get
    parameters that will decide how we connect (see ConnectionManager).
    '''

    def __init__(self, runner, template_manager):
        self._runner = runner
        self._template_manager = template_manager

    def context(self):
        return InventoryContext(self._runner, self._template_manager)


class InventoryContext(object):
    
    def __init__(self, runner, template_manager):
        
        self._runner = runner
        self._template_manager = template_manager

        self._changed = True
        self._default_variables = {}
        self._host_variables = {}
        self._module_variables = {}
        self._facts_for_host = {}
        self._remote_user = {}
        self._host_vars_proxy = None
        self._group_names = []
        self._groups = []
        self._environment = {}
        self._playbook_dir = ""
        self._inventory_dir = ""
        self._inventory_file = ""
        self._item = None

    def set_default_variables(self, value):
        self._changed = True
        self._default_variables = value

    def set_host_variables(self, value):
        self._changed = True
        self._host_variables = value
    
    def set_module_variables(self, value):
        self._changed = True
        self._module_variables = value

    def set_facts_for_host(self, value):
        self._changed = True
        self._facts_for_host = value

    def set_remote_user(self, value):
        self._changed = True
        self._remote_user = value

    def set_host_vars_proxy(self, value):
        self._changed = True
        self._host_vars_proxy = value

    def set_group_names(self, inventory):
        self._changed = True
        self._group_names = self._host_variables.get('group_names', [])

    def set_groups(self, inventory):
        self._changed = True
        self._groups_list = inventory.groups_list()

    def set_remote_user(self, runner):
        self._changed = True
        self._remote_user = runner.remote_user

    def set_module_variables(self, runner):
        self._changed = True
        self._module_variables = runner.module_vars

    def set_default_variables(self, runner):
        self._changed = True
        self._default_variables = runner.default_vars

    def set_environment(self, runner):
        self._changed = True
        self._environment = runner.environment

    def set_playbook_dir(self, runner):
        self._changed = True
        self._playbook_dir = runner.basedir

    def set_inventory_dir(self, inventory):
        self._changed = True
        self._inventory = inventory.basedir()

    def set_inventory_file(self, inventory):
        self._changed = True
        self._inventory_file = inventory.src()

    def set_loop_item(self, value):
        self._changed = True
        self._item = value

    def get_loop_item(self):
        self._changed = True
        return self._item

    def _fetch_and_template(self, field, *args):
        ''' lookup a value from the librarian and then template the result using the host variables '''

        assert isinstance(field, basestring)
        return self.template_manager.template(
            self.get(field, *args),
            self
        )

    def get_delegate_host(self, context):
        hostname = context.get('delegate_to')
        if hostname is not None:
            hostname = self.template_manager.template(hostname, context)
            return self.inventory.get_host(hostname)
        return None

    def get_actual_host(self, host, context):
        return self._fetch_and_template('ansible_ssh_host', 'FIXME DEFAULT GOES HERE')

    def get_actual_user(self, host, context):
        return self._fetch_and_template('ansible_ssh_user', 'FIXME DEFAULT GOES HERE')

    def get_actual_port(self, host, context):
        return self._fetch_and_template('ansible_ssh_host', 'FIXME DEFAULT GOES HERE')

    def get_actual_pass(self, host, context):
        return self._fetch_and_template('ansible_ssh_pass', 'FIXME DEFAULT GOES HERE')

    def get_actual_transport(self, host, context):
        return self._fetch_and_template('ansible_ssh_connection', 'FIXME DEFAULT GOES HERE')

    def get_actual_private_key_file(self, host, context):
        return self._fetch_and_template('ansible_ssh_private_key_file', 'FIXME DEFAULT GOES HERE')

    def calculate(self):
        ''' build the internal variable dictionary '''

        inject = {}
        inject = utils.combine_vars(inject, self._default_variables)
        inject = utils.combine_vars(inject, self._host_variables)
        inject = utils.combine_vars(inject, self._module_variables)
        inject = utils.combine_vars(inject, self._facts_for_host)

        inject.setdefault('ansible_ssh_user', self._remote_user)

        inject['hostvars']     = self._host_vars_proxy
        inject['group_names']  = self._group_names
        inject['groups']       = self._groups_list
        inject['vars']         = self._module_variables
        inject['defaults']     = self._default_variables
        inject['environment']  = self._environment
        inject['playbook_dir'] = self._playbook_dir
        inject['item']         = self._item

        print "INJECT=%s" % inject

        self._inject = inject
        return inject


    def get(self, key, *args):
        assert isinstance(key, basestring)

        ''' Look up the basic value of a variable from inventory (mixing in playbook variables and so on)'''
        if self._changed:
            self._changed = False
            return self.calculate().get(key, *args)        
        else:
            return self._inject.get(key, *args)


