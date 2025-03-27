from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


@tagged('post_install', '-at_install', 'post_install_l10n_in_payroll_config')
class TestHrContractSalaryComponents(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.employee = cls.env['hr.employee'].create({'name': 'Test Employee'})
        cls.contract = cls.env['hr.contract'].create({
            'name': 'Test Contract',
            'wage': 100000.0, 
            'employee_id': cls.employee.id,
            'l10n_in_gratuity_percent': 5.0,
        })

    def test_compute_l10n_in_basic_salary(self):
        self.contract.l10n_in_basic_salary_percent = 40.0
        self.assertEqual(self.contract.l10n_in_basic_salary, 40000.0)
        self.assertEqual(self.contract.l10n_in_hra, 20000.0)
        self.assertEqual(self.contract.l10n_in_performance_bonus, 8000.0)
        self.assertEqual(self.contract.l10n_in_leave_travel_allowance, 8000.0)
        self.assertEqual(self.contract.l10n_in_gratuity_percent, 6.25)
        self.assertEqual(self.contract.l10n_in_supplementary_allowance, 17333.0)

    def test_inverse_l10n_in_basic_salary(self):
        self.contract.l10n_in_basic_salary = 30000.0
        self.assertEqual(self.contract.l10n_in_basic_salary_percent, 30.0)

    def test_compute_l10n_in_hra(self):
        self.contract.l10n_in_hra_percent = 40.0
        self.assertEqual(self.contract.l10n_in_hra, 20000.0)

    def test_inverse_l10n_in_hra(self):
        self.contract.l10n_in_hra = 10000.0
        self.assertEqual(self.contract.l10n_in_hra_percent, 20.0)

    def test_compute_l10n_in_performance_bonus(self):
        self.contract.l10n_in_performance_bonus_percent = 10.0
        self.assertEqual(self.contract.l10n_in_performance_bonus, 5000.0)

    def test_inverse_l10n_in_performance_bonus(self):
        self.contract.l10n_in_performance_bonus = 5000.0
        self.assertEqual(self.contract.l10n_in_performance_bonus_percent, 10.0)

    def test_compute_l10n_in_leave_travel_allowance(self):
        self.contract.l10n_in_leave_travel_allowance_percent = 5.0
        self.assertEqual(self.contract.l10n_in_leave_travel_allowance, 2500.0)

    def test_inverse_l10n_in_leave_travel_allowance(self):
        self.contract.l10n_in_leave_travel_allowance = 2500.0
        self.assertEqual(self.contract.l10n_in_leave_travel_allowance_percent, 5.0)

    def test_compute_l10n_in_std_allowance_percent(self):
        self.contract.l10n_in_std_allowance = 10000.0
        self.assertEqual(self.contract.l10n_in_std_allowance_percent, 10.0)

    def test_inverse_l10n_in_std_allowance_percent(self):
        self.contract.l10n_in_std_allowance_percent = 15.0
        self.assertEqual(self.contract.l10n_in_std_allowance, 15000.0)

    def test_compute_l10n_in_gratuity_percent(self):
        self.contract.l10n_in_gratuity = 2500.0 
        self.assertEqual(self.contract.l10n_in_gratuity_percent, 5.0)

    def test_inverse_l10n_in_gratuity_percent(self):
        self.assertEqual(self.contract.l10n_in_gratuity, 2500.0)

    def test_compute_l10n_in_leave_allowance(self):
        self.contract.l10n_in_leave_allowance_percent = 2.0
        self.assertEqual(self.contract.l10n_in_leave_allowance, 2000.0)

    def test_inverse_l10n_in_leave_allowance(self):
        self.contract.l10n_in_leave_allowance = 3000.0
        self.assertEqual(self.contract.l10n_in_leave_allowance_percent, 3.0)

    def test_compute_l10n_in_supplementary_allowance(self):
        self.contract.write({
            'l10n_in_hra': 20000.0,
            'l10n_in_performance_bonus': 4000.0,
            'l10n_in_leave_travel_allowance': 2000.0,
            'l10n_in_std_allowance': 10000.0,
            'l10n_in_leave_allowance': 2000.0,
        })
        self.assertEqual(self.contract.l10n_in_supplementary_allowance, 9500.0)

    def test_compute_l10n_in_supplementary_allowance_percent(self):
        self.contract.l10n_in_supplementary_allowance = 20000.0
        self.assertEqual(self.contract.l10n_in_supplementary_allowance_percent, 20.0)

    def test_inverse_l10n_in_supplementary_allowance_percent(self):
        self.contract.l10n_in_supplementary_allowance_percent = 25.0
        self.assertEqual(self.contract.l10n_in_supplementary_allowance, 25000.0)
