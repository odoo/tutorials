from dateutil.relativedelta import relativedelta
from psycopg2 import IntegrityError

from odoo.exceptions import UserError
from odoo.fields import Date, Datetime
from odoo.tests import TransactionCase, tagged
from odoo.tools import mute_logger


@tagged("post_install", "-at_install")
class TestEstateProperty(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create test partners
        cls.buyer = cls.env["res.partner"].create(
            {
                "name": "John Buyer",
                "email": "john.buyer@example.com",
            }
        )
        cls.salesperson = cls.env["res.users"].create(
            {
                "name": "Agent Smith",
                "login": "agent_smith",
                "email": "agent.smith@example.com",
            }
        )

        # Create test property type and tags
        cls.property_type = cls.env["estate.property.type"].create(
            {
                "name": "Residential Villa",
            }
        )
        cls.tag_garden = cls.env["estate.property.tag"].create(
            {
                "name": "Garden",
            }
        )

        # Create base test property
        cls.property = cls.env["estate.property"].create(
            {
                "name": "Test Villa",
                "expected_price": 100000.0,
                "sale_mode": "auction",
                "property_type_id": cls.property_type.id,
                "tag_ids": [(6, 0, [cls.tag_garden.id])],
                "salesperson_id": cls.salesperson.id,
            }
        )

    def test_01_property_creation_defaults(self):
        """Test property creation with default values and proper attributes"""
        self.assertEqual(self.property.name, "Test Villa")
        self.assertEqual(self.property.expected_price, 100000.0)
        self.assertEqual(self.property.state, "new")
        self.assertEqual(self.property.bedrooms, 2)
        self.assertTrue(self.property.active)

        # Verify date_availability is set 3 months in the future by default
        expected_date = Date.context_today(self.env.user) + relativedelta(months=3)
        self.assertEqual(self.property.date_availability, expected_date)

    @mute_logger("odoo.sql_db")
    def test_02_property_creation_zero_expected_price_fails(self):
        with self.assertRaises(IntegrityError):
            self.env["estate.property"].create(
                {
                    "name": "Zero Price House",
                    "expected_price": 0.0,
                }
            )

    def test_03_total_area_computation(self):
        self.property.write(
            {
                "living_area": 120,
                "garden_area": 40,
            }
        )
        self.assertEqual(self.property.total_area, 160)

    def test_04_start_auction_validation_and_state(self):
        with self.assertRaises(UserError):
            self.property.action_start_auction()

        self.property.auction_end_time = Datetime.now() + relativedelta(days=5)
        self.property.action_start_auction()

        self.assertEqual(self.property.auction_state, "blocked")

    def test_05_accept_offer_creates_booking_and_updates_property(self):
        offer = self.env["estate.property.offer"].create(
            {
                "property_id": self.property.id,
                "price": 120000.0,
                "partner_id": self.buyer.id,
            }
        )

        offer.action_accept()

        self.assertEqual(offer.status, "accepted")
        self.assertEqual(self.property.selling_price, 120000.0)
        self.assertEqual(self.property.buyer_id, self.buyer)
        self.assertEqual(self.property.state, "pending_booking")

        booking = self.env["estate.booking"].search(
            [("property_id", "=", self.property.id)]
        )
        self.assertTrue(booking.exists())
        self.assertEqual(booking.final_price, 120000.0)
        self.assertEqual(booking.buyer_id, self.buyer)

    def test_06_action_sold_and_cancel_state_guards(self):
        """Test action_sold and action_cancel status guards"""
        self.property.action_sold()
        self.assertEqual(self.property.state, "sold")
        self.assertEqual(self.property.auction_state, "done")

        with self.assertRaises(UserError):
            self.property.action_cancel()
