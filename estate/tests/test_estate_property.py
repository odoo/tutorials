from odoo.tests import TransactionCase, tagged


@tagged("-at_install", "post_install")
class TestPropertyAction(TransactionCase):
    def test_some_action(self):
        record = self.env["estate.property"].create({"expected_price": 100})
        record.action_sold()
        self.assertEqual(record.state, "sold")
