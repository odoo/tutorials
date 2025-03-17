from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class TestSaleSubscriptionPlan(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.subscription_plan_model = cls.env['sale.subscription.plan']
    
    def test_sequence_assignment(self):
        """Test that the sequence is correctly assigned based on billing_period_unit."""
        plan_year = self.subscription_plan_model.create({'billing_period_unit': 'year'})
        plan_month = self.subscription_plan_model.create({'billing_period_unit': 'month'})
        plan_week = self.subscription_plan_model.create({'billing_period_unit': 'week'})

        self.assertEqual(plan_week.sequence, 1, "Week should have sequence 1")
        self.assertEqual(plan_month.sequence, 2, "Month should have sequence 2")
        self.assertEqual(plan_year.sequence, 3, "Year should have sequence 3")

    def test_sequence_recompute_on_update(self):
        """Test that the sequence is updated correctly when billing_period_unit changes."""
        plan = self.subscription_plan_model.create({'billing_period_unit': 'week'})
        self.assertEqual(plan.sequence, 1, "Initial sequence should be 1 for week")
        
        plan.billing_period_unit = 'year'
        plan._compute_sequence()
        self.assertEqual(plan.sequence, 3, "Updated sequence should be 3 for year")
