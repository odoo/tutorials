from odoo import Command
from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from odoo.tests.form import Form


# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.
@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.buyer_partner = cls.env['res.users'].create({
            'name': 'some guy',
            'login': 'some guy login',
        })

        sold_property_with_accepted_offer = {
            "name": "property1",
            "expected_price": "110.0",
            "selling_price": "100.0",
            "offer_ids": [Command.create({"name": "first offer", "price": "1100.0", "status": "accepted", "partner_id": cls.buyer_partner.partner_id.id})],
        }
        cls.properties = cls.env['estate.property'].create([sold_property_with_accepted_offer])
        cls.properties.write({"state": "sold"})

        property_with_no_offer = {
                    "name": "property2",
                    "expected_price": "110.0",
                    "selling_price": "100.0",
                    "offer_ids": [],
                }
        cls.env['estate.property'].create([property_with_no_offer])

    def test_create_offer_on_sold(self):
        sold_property_with_accepted_offer = self.properties.search([("name", "=", "property1")])

        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create({
                "name": "invalid offer",
                "price": "1200.0",
                "property_id": sold_property_with_accepted_offer.id,
                "partner_id": self.buyer_partner.partner_id.id,
            })

    def test_no_sell_with_no_offer(self):
        property_with_no_offer = self.properties.search([("name", "=", "property2")])
        with self.assertRaises(UserError):
            property_with_no_offer.write({
                "state": "sold",
            })

    def test_is_sold_property_marked(self):
        sold_property_with_accepted_offer = self.properties.search([("name", "=", "property1")])
        self.assertRecordValues(sold_property_with_accepted_offer, [{"state": "sold"}])

        property_with_no_offer = self.properties.search([("name", "=", "property2")])
        self.assertRecordValues(property_with_no_offer, [{"state": "new"}])

    def test_garden_reset(self):
        property_with_no_offer = self.properties.search([("name", "=", "property2")])
        self.assertRecordValues(property_with_no_offer, [{"garden_area": 0, "garden_orientation": False, "garden": False}])
        with Form(property_with_no_offer) as property_form:
            property_form.garden = True
            property = property_form.save()
            self.assertRecordValues(property, [{"garden_area": 10, "garden_orientation": "north", "garden": True}])
