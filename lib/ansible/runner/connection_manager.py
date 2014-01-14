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

class ConnectionManager(object):

    ''' 
    The connection manager is responsible for instantiating the connection object.
    '''


    def __init__(self, inventory_librarian):
        self.inv = inventory_librarian

    # ------------------------------------------------------------------


    def get_connection(self, runner, context):

        assert type(host) is inventory.Host
       
        base = connection.Connection(runner)

        delegate_host = self.inv.get_delegate_host(context)

        conn = base.connect(
            self.inv.get_actual_host(context),
            self.inv.get_actual_port(context),
            self.inv.get_actual_user(context),
            self.inv.get_actual_pass(context),
            self.inv.get_actual_transport(context),
            self.inv.get_actual_private_key_file(context),           
        )
        
        if delegate_host:
            conn.delegate = delegate_host

        return conn

    

    
