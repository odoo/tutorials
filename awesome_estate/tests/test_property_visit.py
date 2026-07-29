from odoo.tests import TransactionCase, tagged
from datetime import datetime, timedelta
from odoo import fields


@tagged('standard')
class TestAwesomeEstateVisit(TransactionCase):
    """Test property visit scheduling and overlap logic."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Property = cls.env['awesome.estate.property']
        cls.Visit = cls.env['awesome.estate.property.visit']
        cls.Partner = cls.env['res.partner']

        cls.customer = cls.Partner.create({'name': 'Visitor'})

        cls.property = cls.Property.create(
            {'name': 'Visit Test', 'expected_price': 100000, 'living_area': 80}
        )

        cls.visit = cls.Visit.create(
            {
                'property_id': cls.property.id,
                'customer_id': cls.customer.id,
                'visit_time_start': fields.Datetime.now() + timedelta(hours=24),
                'visit_time_end': fields.Datetime.now() + timedelta(hours=25),
            }
        )

    def test_visit_default_state(self):
        self.assertEqual(self.visit.state, 'scheduled')

    def test_visit_duration_compute(self):
        self.assertAlmostEqual(self.visit.duration, 1.0, places=1)

    def test_visit_is_today_false_for_future(self):
        self.assertFalse(self.visit.is_today)

    def test_visit_is_mine(self):
        """Visit created by another user should not be 'mine'."""
        Visit = self.Visit.sudo(self.env['res.users'].create({
            'name': 'Other Agent',
            'login': 'other_agent_visit',
            'password': 'password',
        }))
        other_visit = Visit.create({
            'property_id': self.property.id,
            'customer_id': self.customer.id,
            'visit_time_start': fields.Datetime.now() + timedelta(hours=48),
            'visit_time_end': fields.Datetime.now() + timedelta(hours=49),
        })
        self.assertFalse(other_visit.is_mine)
