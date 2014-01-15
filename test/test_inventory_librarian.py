import unittest
from nose.plugins.skip import SkipTest
import os

from ansible.runner.inventory_librarian import InventoryLibrarian

# default variables are variables that come in from things like role
# defaults and have a lower priority than inventory variables
DEFAULT_VARIABLES = dict(
   a = 1,
   from_default_vars = 1,
   expect_host_vars_to_clobber = 0,
   expect_module_vars_to_clobber = -1
)

# module vars are task parameters like 'ignore_errors' or 'always_run' and usually
# don't replace any user variables or system facts
MODULE_VARIABLES = dict(
   a = 3,
   b = 4,
   c = 5,
   from_module_vars = 1,
   expect_module_vars_to_clobber = 1,
   expect_host_facts_to_clobber = 0
)

REMOTE_USER = 'remote_user'

GROUPS_LIST = [ 'web', 'db', 'file', 'build' ]

ENVIRONMENT = dict(
   enva = "8",
   envb = "9"
)

BASEDIR = '/tmp'

class MockRunner():
    def __init__(self):
        self.default_vars = DEFAULT_VARIABLES
        self.module_vars  = MODULE_VARIABLES
        self.remote_user  = REMOTE_USER
        self.environment  = ENVIRONMENT
        self.basedir      = BASEDIR

class MockTemplateManager():
    pass

class MockHostVarsProxy():
    pass

class MockInventory():

    def __init__(self):
        pass

    def groups_list(self):
        return GROUPS_LIST

    def basedir(self):
        return BASEDIR
 
    def src(self):
        return os.path.join(BASEDIR, 'test.yml')

# =================================


# host variables are variables that came from inventory
HOST_VARIABLES = dict(
   a = 2,
   b = 3,  
   from_host_vars = 1,
   expect_host_vars_to_clobber = 1,
   expect_module_vars_to_clobber = 0
)


# host facts are from setup or custom fact modules, or operations like 'register'
HOST_FACTS = dict(
   a = 4,
   b = 5,
   c = 6,
   d = 7,
   from_host_facts = 1,
   expect_host_facts_to_clobber = 1
)




class TestInventoryLibrarian(unittest.TestCase):


    def setUp(self):

        self.mock_inventory = MockInventory()
        self.mock_runner = MockRunner()
        self.mock_template_manager = MockTemplateManager()
        self.mock_host_vars_proxy = MockHostVarsProxy()
        self.librarian = InventoryLibrarian(self.mock_runner, self.mock_template_manager)
        self.context = self.librarian.context()

    def basic_prep(self): 
        self.context.set_host_variables(HOST_VARIABLES)
        self.context.set_facts_for_host(HOST_FACTS)
        self.context.set_host_vars_proxy(self.mock_host_vars_proxy)
        self.context.set_inventory(self.mock_inventory)
        self.context.set_loop_item(None)
        
    def test_basic_variable_blending(self):
        self.basic_prep()
        results = self.context.calculate()

        assert results['a'] == 4
        assert results['environment'] == ENVIRONMENT
        assert results['from_default_vars'] == 1
        assert results['expect_module_vars_to_clobber'] ==1
        assert results['d'] == 7

        assert isinstance(results['hostvars'], MockHostVarsProxy)
        assert results['from_host_vars'] == 1
        assert results['expect_host_vars_to_clobber'] == 1
        assert results['expect_host_vars_to_clobber'] == 1

        print results['group_names']
        assert results['group_names'] == GROUPS_LIST
        assert 'defaults' in results
        assert 'vars' in results
        assert playbook_dir == BASEDIR
        assert results['ansible_ssh_user'] == REMOTE_USER

        # TODO: not in this file, but we want some real tests for inventory precedence.
        # this does not need to contain that.




 
