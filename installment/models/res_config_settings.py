from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    max_duration = fields.Float(
        string="Max Duration (Years)",
        config_parameter="installment.max_duration",
        required=True,
    )
    annual_rate = fields.Float(
        string="Annual Rate Percentage", config_parameter="installment.annual_rate"
    )
    down_payment_percentage = fields.Float(
        string="Down Payment Percentage",
        config_parameter="installment.down_payment_percentage",
    )
    admin_expenses_percentage = fields.Float(
        string="Administrative Expenses Percentage",
        config_parameter="installment.admin_expenses_percentage",
    )
    delay_penalty_percentage = fields.Float(
        string="Delay Penalty Percentage",
        config_parameter="installment.delay_penalty_percentage",
    )
    delay_penalty_process = fields.Float(
        string="Delay Penalty Process (Days)",
        config_parameter="installment.delay_penalty_process",
    )
    nid = fields.Boolean(string="NID", config_parameter="installment.nid")
    bank_statement = fields.Boolean(
        string="Bank Statement", config_parameter="installment.bank_statement"
    )
    rental_contract = fields.Boolean(
        string="Rental Contract",
        config_parameter="installment.rental_contract",
    )
    salary_components = fields.Boolean(
        string="Salary Components",
        config_parameter="installment.salary_components",
    )
    bank_rate_letter = fields.Boolean(
        string="Bank Rate Letter",
        config_parameter="installment.bank_rate_letter",
    )
    ownership_contract = fields.Boolean(
        string="Ownership Contract",
        config_parameter="installment.ownership_contract",
    )
