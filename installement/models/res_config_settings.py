from odoo import models, fields


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    max_duration = fields.Integer(
        string="Max Duration", config_parameter='installement.max_duration')
    annual_rate_percentage = fields.Integer(
        string='Annual Rate Percentage', config_parameter='installement.annual_rate_percentage')
    down_payment_percentage = fields.Integer(
        string="Down Payment Percentage", config_parameter='installement.down_payment_percentage')
    administrative_expenses_percentage = fields.Integer(
        string='Administrative Expenses Percentage', config_parameter='installement.administrative_expenses_percentage')
    delay_penalty_percentage = fields.Integer(
        string="Delay Penalty Percentage", config_parameter='installement.delay_penalty_percentage')
    delay_penalty_process = fields.Integer(
        string='Delay Penalty Process', config_parameter='installement.delay_penalty_process')

    nid = fields.Boolean("Nid")
    salary_component = fields.Boolean('Salary Component')
    bank_statement = fields.Boolean('Bank Statement')
    bank_rate_letter = fields.Boolean('Bank Rate Letter')
    rental_contract = fields.Boolean('Rental Contract')
    ownership_contract = fields.Boolean('Ownership Contract')
