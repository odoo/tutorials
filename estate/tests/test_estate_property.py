from odoo.exceptions import UserError
from odoo.tests import Form,tagged, TransactionCase


@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()

        cls.properties = cls.env["estate.property"].create(
            [{"name": "Property 1", "state": "new", "expected_price": 10}]
        )
        cls.partner_id = cls.env['res.partner'].create({'name': 'Raju Rastogi'})
        cls.offer1 = cls.env["estate.property.offer"].create(
            [
                {
                    "property_id": cls.properties.id,
                    "partner_id": cls.partner_id.id,
                    "price": 1000,
                    "status": "accepted",
                }
            ]
        )

    def test_create_offer_for_a_sold_property(self):
        print(
            "-------------------------------1------------------------------------------"
        )
        self.properties.state = "sold"
        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create(
                [
                    {
                        "property_id": self.properties.id,
                        "partner_id": self.partner_id.id,
                        "price": 20000,
                    }
                ]
            )

    def test_sell_a_property_with_no_accepted_offers(self):
        print(
            "------------------------------2-----------------------------------------"
        )
        self.offer1.status = "refused"
        with self.assertRaises(UserError):
            self.properties.action_sold()

    def test_sold_is_correctly_marked(self):
        self.offer1.action_confirm()
        self.properties.action_sold()
        self.assertEqual(
            self.properties.state,
            "sold",
            "Property Should be marked as sold after selling it.",
        )

    def test_uncheck_check_garden_checkbox(self):
        estate_form = Form(self.properties)

        estate_form.garden = False
        self.assertEqual(estate_form.garden_orientation, False)
        self.assertEqual(estate_form.garden_area, 0)
        print(estate_form.garden_area)
        print(estate_form.garden_orientation)
        print("UNcheck funtion")

        estate_form.garden = True
        self.assertEqual(estate_form.garden_orientation, "north")
        self.assertEqual(estate_form.garden_area, 10)
        print(estate_form.garden_area)
        print(estate_form.garden_orientation)
        print("check funtion")
