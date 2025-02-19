from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import Form, tagged 


@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()
        cls.property_type = cls.env["estate.property.type"].create(
            {"name": "Apartment"}
        )
        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})
        cls.property = cls.env["estate.property"].create(
            {
                "name": "Test Property",
                "property_type_id": cls.property_type.id,
                "expected_price": 100000,
                "user_id": cls.env.user.id,
                "state": "new",
            }
        )
        cls.offer = cls.env["estate.property.offer"].create(
            {
                "price": 110000,
                "partner_id": cls.partner.id,
                "property_id": cls.property.id,
            }
        )

    def test_prevent_offer_creation_for_sold_property(self):
        print("---------------------------------------1--------------------------------------------------")
        self.property.state = "sold"
        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create(
                {
                    "price": 120000,
                    "partner_id": self.partner.id,
                    "property_id": self.property.id,
                }
            )

    def test_prevent_selling_property_without_accepted_offer(self):
        print("---------------------------------------2--------------------------------------------------")
        self.offer.write({"status": "refused"})
        with self.assertRaises(UserError):
            self.property.action_property_sold()

    def test_property_is_marked_as_sold(self):
        print("---------------------------------------3--------------------------------------------------")
        self.offer.action_offer_confirm()
        self.property.action_property_sold()
        self.assertEqual(self.property.state,"sold","Property Should be marked as sold after selling it.")

    def test_garden_checkbox_reset(self):
        print("----------------------------------------4------------------------------------------------")
        with Form(self.property) as form:
            form.garden = True
            print(form.user_id.name)
            print(form.garden_area)
            print(form.garden_orientation)
            form.garden = False
            print(form.garden_area)
            print(form.garden_orientation)
            self.assertEqual(form.garden_area, 0, "Garden Area should be reset to 0 when Garden checkbox is unchecked")
            self.assertEqual(form.garden_orientation, False, "Garden Orientation should be reset to False when Garden checkbox is unchecked")

    