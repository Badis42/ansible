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

import ansible.utils.template as utils_template

class TemplateManager(object):
    ''' 
    The template manager works to template various strings.

    Initially this will just be an OO wrapper around utils functions, though this will eventually be a home for logic from
    those classes as we roll them up into this class.
    '''

    def __init__(self, basedir):
        self.basedir = basedir

    def template(self, str, context):
        variable_dict = context.calculate()
        return utils_template.template(self.basedir, str, variable_dict, fail_on_undefined=True)


