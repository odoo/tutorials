from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError
from odoo.tests import tagged, Form, TransactionCase


@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()
        cls.property = cls.env["estate.property"].create(
            [{"name": "Property 1", "status": "new", "expected_price": 10}]
        )

        cls.property_test= cls.env["estate.property"].create(
            [{"name": "Demo Property", "status": "new", "expected_price": 100}]
        )

        cls.partner_id = cls.env["res.partner"].create({"name": "Demo Partner"})

        cls.offer1 = cls.env["estate.property.offer"].create(
            [
                {
                    "property_id": cls.property.id,
                    "partner_id": cls.partner_id.id,
                    "price": 1000,
                    "status_offer": "accepted",
                }
            ]
        )

        cls.offer2 = cls.env["estate.property.offer"].create(
            [
                {
                    "property_id": cls.property_test.id,
                    "partner_id": cls.partner_id.id,
                    "price": 1000,
                    "status_offer": "accepted",
                }
            ]
        )
        cls.offer2.accept_offer()

    def test_create_offer_for_a_sold_property(self):
        self.property_test.sold_event()
        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create(
                [
                    {
                        "property_id": self.property_test.id,
                        "partner_id": self.partner_id.id,  
                        "price": 20000,
                    }
                ]
            )

    def test_sell_a_property_with_no_accepted_offers(self):
        self.offer1.status_offer = "refused"
        with self.assertRaises(UserError):
            self.property.sold_event()

    def test_sold_is_correctly_marked(self):
        print(self.property.status)
        self.offer1.accept_offer()
        print(self.property.status)
        self.property.sold_event()
        self.assertEqual(
            self.property.status,
            "sold",
            "Property Should be marked as sold after selling it",
        )

    def test_garden_onchange_reset_and_resotre(self):
        estate_form = Form(self.property)
        estate_form.garden = True
        self.assertEqual(estate_form.garden_area, 1000)
        self.assertEqual(estate_form.garden_orientation, "north")
        print(estate_form.garden_area, " ", estate_form.garden_orientation)
        estate_form.garden = False
        self.assertEqual(estate_form.garden_area, 0)
        self.assertEqual(estate_form.garden_orientation, False)
        print(estate_form.garden_area, " ", estate_form.garden_orientation)
