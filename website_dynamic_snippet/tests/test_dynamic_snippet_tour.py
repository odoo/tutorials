from odoo.tests import HttpCase, tagged

@tagged('post_install', '-at_install')
class TestDynamicSnippetTour(HttpCase):
    def test_dynamic_snippet_tour(self):
        self.start_tour("/", "website_dynamic_snippet.sale_order_snippet", login="admin", watch=True)
