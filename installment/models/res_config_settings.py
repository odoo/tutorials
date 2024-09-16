from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    max_duration = fields.Integer(string="Max Duration", config_parameter="installment.max_duration")
    annual_rate_percentage = fields.Integer(string="Annual Rate Percentage", config_parameter="installment.annual_rate_percentage")
    down_payment_percentage = fields.Integer(string="Down Payment Percentage", config_parameter="installment.down_payment_percentage")
    administrative_expense_percentage = fields.Integer(string="Administrative Expense Percentage", config_parameter="installment.administrative_expense_percentage")
    delay_penalty_percentage = fields.Integer(string="Delay Penalty Percentage", config_parameter="installment.delay_penalty_percentage")
    delay_penalty_process = fields.Integer(string="Delay Penalty Process", config_parameter="installment.delay_penalty_process")

    nid = fields.Boolean(string="NID", config_parameter="installment.nid")
    bank_statement = fields.Boolean(string="Bank Statement", config_parameter="installment.bank_statement")
    rental_contract = fields.Boolean(string="Rental Contract", config_parameter="installment.rental_contract")
    salary_components = fields.Boolean(string="Salary Components", config_parameter="installment.salary_components")
    bank_rate_letter = fields.Boolean(string="Bank Rate Letter", config_parameter="installment.bank_rate_letter")
    ownership_contract = fields.Boolean(string="Ownership Contract", config_parameter="installment.ownership_contract")