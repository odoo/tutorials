from odoo import models, fields


class InstallmentSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    max_duration = fields.Float('Max Duration', config_parameter="installments.max_duration")
    annual_rate = fields.Float('Annual Rate', config_parameter="installments.annual_rate")
    down_payment_perc = fields.Float('Down Payment', config_parameter="installments.down_payment_perc")
    admin_exp_perc = fields.Float('Administrative Expenses', config_parameter="installments.admin_exp_perc")
    delay_penalty_perc = fields.Float('Delay Penalty', config_parameter="installments.delay_penalty_perc")
    delay_penalty_process = fields.Integer('Delay Penalty Process', config_parameter="installments.delay_penalty_process")
    nid = fields.Boolean('Nid', config_parameter="installments.nid")
    bank_statement = fields.Boolean('Bank Statement', config_parameter="installments.bank_statement")
    rental_contract = fields.Boolean('Rental Contract', config_parameter="installments.rental_contract")
    salary_components = fields.Boolean('Salary Components', config_parameter="installments.salary_components")
    bank_rate_letter = fields.Boolean('Bank Rate Letter', config_parameter="installments.bank_rate_letter")
    owernship_contract = fields.Boolean('Ownership Contract', config_parameter="installments.owernship_contract")
