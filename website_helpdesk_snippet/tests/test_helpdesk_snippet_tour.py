import odoo.tests
from odoo.tests import HttpCase

@odoo.tests.common.tagged('post_install', '-at_install')
class MyCustomTest(HttpCase):
    def test_my_tour(self):
    
        self.start_tour("/", "website_helpdesk_snippet.helpdesk_snippet_tour", login="admin")

