from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged, Form


@tagged("post_install", "-at_install")
class EstateTestOfferCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super().setUpClass()

        cls.property = cls.env["estate.property"].create(
            {
                "name": "Test Property",
                "expected_price": 31,
                "garden": True,
                "garden_area": 300,
                "garden_orientation": "south",
            }
        )

    def test_selling_property_without_an_offer(self):
        """Test that we can't create an offer for a sold property"""
        self.assertFalse(self.property.offer_ids)

        with self.assertRaises(UserError):
            self.property.action_property_sold()

        self.assertTrue(self.property.state == "new")

    def test_sold_property_state_change(self):
        """Test that the state of a sold property automatically changes to sold"""
        self.env["estate.property.offer"].create(
            {
                "price": 67,
                "partner_id": self.env.user.partner_id.id,
                "property_id": self.property.id,
            }
        )
        self.property.action_property_sold()

        self.assertTrue(self.property.state == "sold")

    def test_unchecking_garden_resets_area_and_orientation(self):
        """Verify that unchecking 'garden' resets 'garden_area' and 'garden_orientation' via UI Form."""
        with Form(self.property) as prop_form:
            # Check the garden box and modify area & orientation
            prop_form.garden = True
            prop_form.garden_area = 150
            prop_form.garden_orientation = "north"

            # Check 1
            self.assertEqual(prop_form.garden_area, 150)
            self.assertEqual(prop_form.garden_orientation, "north")

            # 3. Uncheck garden (this automatically fires the @api.onchange('garden'))
            prop_form.garden = False

            # Check if areas are cleared
            self.assertEqual(prop_form.garden_area, 0)
            self.assertTrue(prop_form.garden_orientation == "n/a")

        property_record = prop_form.save()
        self.assertEqual(property_record.garden_area, 0)
        self.assertTrue(property_record.garden_orientation == "n/a")
