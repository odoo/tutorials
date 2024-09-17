from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    max_duration = fields.Float(string="Max Duration", config_parameter = "installment.max_duration")
    down_payment = fields.Integer(string="Down Payment Percentage", config_parameter = "installment.down_payment")
    annual_rate = fields.Integer(string="Annual Rate Percentage", config_parameter = "installment.annual_rate")
    administrative_expenses = fields.Integer(
        string="Administrative Expenses Percentage", config_parameter = "installment.administrative_expenses"
    )
    delay_penalty_percentage = fields.Integer(string="Delay Penalty Percentage", config_parameter = "installment.delay_penalty_percentage")
    delay_penalty_process = fields.Integer(string="Delay Penalty Process",config_parameter = "installment.delay_penalty_process")
    nid = fields.Boolean(config_parameter = "installment.nid")
    salary_components = fields.Boolean(string="Salary Components", config_parameter = "installment.salary_components")
    bank_statement = fields.Boolean(string="Bank Statement", config_parameter = "installment.bank_statement")
    bank_rate_letter = fields.Boolean(string="Bank Rate Letter", config_parameter = "installment.bank_rate_letter")
    rental_contract = fields.Boolean(string="Rental Contract", config_parameter = "installment.rental_contract")
    ownership_contract = fields.Boolean(string="Ownershp Contract", config_parameter = "installment.ownership_contract")
