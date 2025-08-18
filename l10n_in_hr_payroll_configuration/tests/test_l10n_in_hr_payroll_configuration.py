from odoo.tests.common import TransactionCase
from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class HrPayrollConfigurationTest(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.employee = cls.env["hr.employee"].search([("name", "=", "Alisha Sharma")])
        cls.company = cls.env["res.company"].search([("name", "=", "IN Company")])
        cls.contract = cls.env["hr.contract"].create(
            {
                "name": "Test Contract",
                "employee_id": cls.employee.id,
                "company_id": cls.company.id,
                "wage": 50000
            }
        )

    def percent_value(self, percent, percentof):
        return percent * percentof

    def test_salary_components_calculation(self):
        self.basic_salary_percent = self.contract.l10n_in_basic_salary_company
        self.hra_percent = self.contract.l10n_in_hra_company
        self.leave_travel_allowance_percent = self.contract.l10n_in_leave_allowance_company
        self.gratuity_percent = self.contract.l10n_in_gratuity_company

        self.basic_salary = self.percent_value(self.basic_salary_percent, self.contract.wage)
        self.hra = self.percent_value(self.hra_percent, self.basic_salary)
        self.leave_travel_allowance = self.percent_value(self.leave_travel_allowance_percent, self.basic_salary)
        self.gratuity = self.percent_value(self.gratuity_percent, self.basic_salary)
        self.assertRecordValues(
            self.contract,
            [
                {
                    "name": "Test Contract",
                    "l10n_in_basic_salary": self.basic_salary,
                    "l10n_in_hra": self.hra,
                    "l10n_in_leave_travel_allowance": self.leave_travel_allowance,
                    "l10n_in_gratuity": self.gratuity
                }
            ]
        )

    def test_supplementary_allowance_calculation(self):
        contract = self.contract
        salary_components = (
            contract.l10n_in_basic_salary
            + contract.l10n_in_hra
            + contract.l10n_in_standard_allowance
            + contract.l10n_in_performance_bonus
            + contract.l10n_in_leave_travel_allowance
            + contract.l10n_in_leave_allowance
            + contract.l10n_in_gratuity
        )
        self.assertEqual(contract.l10n_in_supp_allowance, contract.wage - salary_components)

    def test_basic_salary_percent_calculation(self):
        with self.debug_mode():
            form = Form(self.contract)
            form.l10n_in_basic_salary = 20000
            self.assertEqual(form.l10n_in_basic_salary_company, form.l10n_in_basic_salary / form.wage)
