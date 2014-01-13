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

from ansible import inventory
import connection 

# refactoring notes:
# -- FIXME -- this still needs a lot more logic to deal with the "actual_" logic in the original runner
#             this is just a stub to get us started.

class ConnectionManager(object):

    ''' 
    The connection manager decides what out connection the user would like to use out of what's possible
    and then instantiates the connection.
    '''


    def __init__(self, inventory_librarian, template_manager):

        self.inventory_librarian = inventory_librarian
        self.template_manager    = template_manager

        pass

    # ------------------------------------------------------------------
   
    def _fetch_librarian_value(self, host, context, field):
        ''' lookup the value of a variable from a host or the delegate host '''

        assert type(host) is inventory.Host
        print field
        assert isinstance(field, basestring)

        delegate_host = self.get_delegate_host(context)

        if delegate_host:
            return context.get(delegate_host, 'ansible_ssh_host')
        else:
            return context.get(host, 'ansible_ssh_host')

    # ------------------------------------------------------------------

    def _fetch_and_template(self, host, context, field, *args):
        ''' lookup a value from the librarian and then template the result using the host variables '''

        assert type(host) is inventory.Host
        assert isinstance(field, basestring)

        return self.template_manager.template(
            self._fetch_librarian_value(host, context, field, *args),
            context
        )

    # ------------------------------------------------------------------

    def get_actual_host(self, host, context):
        return self._fetch_and_template(host, context, 'ansible_ssh_host')

    # ------------------------------------------------------------------

    def get_actual_user(self, host, context):
        return self._fetch_and_template(host, context, 'ansible_ssh_user')

    # ------------------------------------------------------------------
          
    def get_actual_port(self, host, context):
        return self._fetch_and_template(host, context, 'ansible_ssh_host')

    # ------------------------------------------------------------------

    def get_actual_pass(self, host, context):
        return self._fetch_and_template(host, context, 'ansible_ssh_pass')

    # ------------------------------------------------------------------

    def get_actual_transport(self, host, context): 
        print "TRANSPORT="
        return self._fetch_and_template(host, context, 'ansible_ssh_connection')

    # ------------------------------------------------------------------

    def get_actual_private_key_file(self, host, context):
        return self._fetch_and_template(host, context, 'ansible_ssh_private_key_file')

    # ------------------------------------------------------------------

    def get_delegate_host(self, context):
        hostname = context.get('delegate_to')
        if hostname is not None:
            hostname = self.template_manager.template(hostname, context) 
            return self.inventory.get_host(hostname)
        return None
 
    # ------------------------------------------------------------------


    def get_connection(self, runner, host, context):

        assert type(host) is inventory.Host
       
        base = connection.Connection(runner)

        delegate_host = self.get_delegate_host(context)

        conn = base.connect(
            self.get_actual_host(host, context),
            self.get_actual_port(host, context),
            self.get_actual_user(host, context),
            self.get_actual_pass(host, context),
            self.get_actual_transport(host, context),
            self.get_actual_private_key_file(host, context),           
        )
        
        if delegate_host:
            conn.delegate = delegate_host

        return conn

    

    
