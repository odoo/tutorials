from odoo.tests.common import TransactionCase
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestHrContract(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.contract = cls.env['hr.contract'].create({
            'name': "Test Contract",
            'wage': 100000,
            'l10n_in_basic_salary_percent': 50,
            'l10n_in_house_rent_allowance_percent': 50,
            'l10n_in_standard_allowance': 4167,
            'l10n_in_performance_bonus_percent': 20,
            'l10n_in_leave_travel_allowance_percent': 20,
            'l10n_in_gratuity': 250,
        })

    def test_salary_component_amounts(self):
        self.assertEqual(self.contract.l10n_in_basic_salary, 50000, "50% of 100000 should be 50000")
        self.assertEqual(self.contract.l10n_in_house_rent_allowance, 25000, "50% of 50000(Basic Salary) should be 25000")
        self.assertEqual(self.contract.l10n_in_standard_allowance_percent, 4.167, "4167 is a 4.17% of 100000(Wage)")
        self.assertEqual(self.contract.l10n_in_performance_bonus, 10000, "20% of 50000(Basic Salary) should be 10000")
        self.assertEqual(self.contract.l10n_in_leave_travel_allowance, 10000, "20% of 50000(Basic Salary) should be 10000")
        self.assertEqual(self.contract.l10n_in_gratuity_percent, 0.50, "250 is a 0.50% of 50000(Basic Salary)")
        self.assertEqual(self.contract.l10n_in_supplementary_allowance, 583, "supplementary should be remaining amount from wage")
