from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Installment Process 
    max_duration = fields.Integer(
        string="Max Duration",
        config_parameter='installment.max_duration'
    )
    annual_rate_percentage = fields.Float(
        string="Annual Rate Percentage (%)",
        config_parameter='installment.annual_rate_percentage'
    )
    down_payment_percentage = fields.Float(
        string="Down Payment Percentage (%)",
        config_parameter='installment.down_payment_percentage'
    )
    admin_expenses_percentage = fields.Float(
        string="Administrative Expenses Percentage (%)",
        config_parameter='installment.admin_expenses_percentage'
    )
    delay_penalty_percentage = fields.Float(
        string="Delay Penalty Percentage (%)",
        config_parameter='installment.delay_penalty_percentage'
    )
    delay_penalty_days = fields.Integer(
        string="Delay Penalty Process (Days)",
        config_parameter='installment.delay_penalty_days'
    )

    # Needed Documents
    nid_required = fields.Boolean(
        string="NID",
        config_parameter='installment.nid_required'
    )
    bank_statement_required = fields.Boolean(
        string="Bank Statement",
        config_parameter='installment.bank_statement_required'
    )
    rental_contract_required = fields.Boolean(
        string="Rental Contract",
        config_parameter='installment.rental_contract_required'
    )
    salary_components_required = fields.Boolean(
        string="Salary Components",
        config_parameter='installment.salary_components_required'
    )
    bank_rate_letter_required = fields.Boolean(
        string="Bank Rate Letter",
        config_parameter='installment.bank_rate_letter_required'
    )
    ownership_contract_required = fields.Boolean(
        string="Ownership Contract",
        config_parameter='installment.ownership_contract_required'
    )
