from datetime import date
from odoo.tests.common import TransactionCase
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrTdsDeclaration(TransactionCase):
    """ Involves necessary test cases of hr_tds_declaration & hr_tds_declaration_details models."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tds_declaration = cls.env["hr.tds.declaration"].create(
            {
                "name": "Test Declaration",
                "financial_year": f"{date.today().year}-{date.today().year}",
                "state": "new",
            }
        )

        cls.declaration_details = cls.env["hr.tds.declaration.details"].create(
            {
                "tds_declaration_id": cls.tds_declaration.id,
                "state": "new",
                "total_income": 1400000,
                "standard_deduction": 75000,
                "other_income_source": 100000,
                "other_allowance": 50000,
            }
        )

    def test_start_end_date_computation(self):
        self.tds_declaration._compute_dates()
        start_year = int(self.tds_declaration.financial_year.split("-")[0])
        end_year = int(self.tds_declaration.financial_year.split("-")[1])

        expected_start_date = date(start_year, 4, 1)
        expected_end_date = date(end_year, 3, 31)

        self.assertEqual(self.tds_declaration.start_date, expected_start_date, "Start Date computation failed.")
        self.assertEqual(self.tds_declaration.end_date, expected_end_date, "End Date computation failed.")

    def test_state_transitions(self):
        self.tds_declaration.action_approved()
        self.assertEqual(self.tds_declaration.state, "accepted", "State transition in action approve failed")

        self.tds_declaration.action_set_to_draft()
        self.assertEqual(self.tds_declaration.state, "draft", "State transition in action set to draft failed")

    def test_tds_declaration_count(self):
        self.tds_declaration._compute_declarations_count()
        self.assertEqual(self.tds_declaration.tds_declaration_count, 1, "TDS declaration count computation failed.")

    def test_action_open_declaration(self):
        action = self.tds_declaration.action_open_declarations()
        self.assertEqual(action["res_model"], "hr.tds.declaration.details", "Incorrect res_model being passed in action.")

    def test_declaration_details_state_transition(self):
        self.declaration_details.action_tds_declaration_confirm()
        self.assertEqual(self.declaration_details.state, "verify", "State transition failed on action of Confirm button.")

        self.declaration_details.action_tds_declaration_approve()
        self.assertEqual(self.declaration_details.state, "approve", "State transition failed on action of Approve button.")

        self.declaration_details.action_tds_declaration_cancel()
        self.assertEqual(self.declaration_details.state, "cancel", "State transition failed on action of Cancel button.")

    def test_tds_calculations(self):
        self.assertEqual(self.declaration_details.total_income, 1550000, "Incorrect Total Income is being calculated.")
        self.assertEqual(self.declaration_details.taxable_amount, 1475000, "Incorrect Total Taxable amount is being calculated.")
        self.assertEqual(self.declaration_details.tax_on_taxable_amount, 135000, "Incorrect Tax payable on Total Taxable amount is being calculated.")
        self.assertEqual(self.declaration_details.total_tax_to_pay, 140400, "Incorrect Total Tax Payable is being calculated.")
        self.assertEqual(self.declaration_details.monthly_tds, 11700, "Incorrect Monthly is being calculated.")
