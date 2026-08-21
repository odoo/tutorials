from odoo.exceptions import ValidationError
from odoo.tests import tagged

from odoo.addons.estate.tests.common import EstatePropertyCommon


@tagged("post_install", "-at_install")
class EstatePropertyOfferCase(EstatePropertyCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        main_property = cls.estate_properties.search([("name", "=", "Property 1")])
        cls.estate_property_offers = cls.env["estate.property.offer"].create([
            {
                "price": 95.0,
                "partner_id": cls.partner.id,
                "property_id": main_property.id,
            },
        ])
        main_property.state = "offer_received"

    def _sell_main_property(cls):
        """Sells the main property with a current offer"""
        main_property = cls.estate_properties.search([("name", "=", "Property 1")])

        if main_property and main_property.offer_ids:
            main_property.offer_ids[0].action_accept()

        main_property.action_sold()

    def test_create_offer_sold_property(self):
        """Test that you can't create an offer for a sold property"""
        self._sell_main_property()

        with self.assertRaises(ValidationError):
            self.env["estate.property.offer"].create([
            {
                "price": 97.0,
                "partner_id": self.partner.id,
                "property_id": self.estate_properties.search([("name", "=", "Property 1")]).id,
            },
        ])

    def test_sell_property_without_offer(self):
        """Test that you can't sell properties that do not have any offer"""
        main_property = self.estate_properties.search([("name", "=", "Property 1")])

        for offer in self.estate_property_offers:
            if offer.property_id.id == main_property.id:
                offer.unlink()

        with self.assertRaises(ValidationError):
            self._sell_main_property()
