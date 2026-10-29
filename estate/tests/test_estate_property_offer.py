from odoo.tests import TransactionCase
from odoo.exceptions import UserError


# @tagged('estatetag')
class EstatePropertyOfferTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.properties = cls.env['estate.property'].create(
            {"state": "new", "name": "House in Mons/Hainaut", "expected_price": 150000.0})
        cls.property_offers = cls.env['estate.property.offer'].create([
            {"property_id": cls.properties.id, "price": 145000},
            {"property_id": cls.properties.id, "price": 150000},
        ])

    def test_estate_property_offer_on_sold_property(self):
        self.property_offers[0].action_accept()
        self.properties.action_sold()
        with self.assertRaises(UserError):
            self.new_offer = self.env['estate.property.offer'].create(
                {"property_id": self.properties.id, "price": 155000}
            )
