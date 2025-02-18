from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()

        cls.properties = cls.env["estate.property"].create({
                "name": "Test property",
                "postcode": 12,
                "expected_price": 1.00,
                "garden": True,
                "garden_area": 50,
                "garden_orientation": "north"
        })

        cls.offer = cls.env["estate.property.offer"].create({
                "price": 20.00,
                "property_id": cls.properties.id,
                "partner_id": cls.env.ref("base.res_partner_12").id,
        })

    def test_prevent_offer_on_sold_property(self):
        """Test that an offer cannot be created for a sold property."""
        self.properties.state = "sold"  # Manually set the property as sold

        with self.assertRaises(UserError, msg="Cannot create offer on a sold property"):
            self.env["estate.property.offer"].create({
                    "price": 1950.00,
                    "property_id": self.properties.id,
                    "partner_id": self.env.ref("base.res_partner_12").id,
            })

    def test_prevent_selling_without_accepted_offer(self):
        """Test that a property cannot be sold if no offer is accepted."""
        with self.assertRaises(
            UserError, msg="Cannot sell a property without an accepted offer"):
            self.properties.action_to_sold_property()

    def test_successful_property_sale(self):
        """Test that a property sold is correctly marked as sold or not."""
        self.offer.status = "accepted"
        self.properties.action_to_sold_property()

        self.assertEqual(
            self.properties.state,
            "sold",
            "Property should be marked as sold after successful sale",
        )
    
    def test_garden_reset_working(self):
        """ Test that ensures values reflecting properly on unchecking garden checkbox."""
        test_garden = Form(self.properties)
        test_garden.garden = False

        test_garden.assertEqual(test_garden.garden_orientation,'',"Garden orienatation should be cleared when garden is unchecked.")
        test_garden.assertEqual(test_garden.garden_area,0,"Garden area should be reset to 0.")


