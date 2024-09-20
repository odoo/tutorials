from odoo import fields, models


class installment(models.TransientModel):
    _inherit = "res.config.settings"

    name = fields.Char()
    max_duration = fields.Float(config_parameter="installment.max_duration")
    annual_percentage_rate = fields.Float(
        config_parameter="installment.annual_percentage_rate"
    )
    down_payment_percentage = fields.Float(
        config_parameter="installment.down_payment_percentage"
    )
    administrative_expenses_percentage = fields.Float(
        config_parameter="installment.administrative_expenses_percentage"
    )
    down_penalty_percentage = fields.Float(
        config_parameter="installment.down_penalty_percentage"
    )
    delay_penalty_process = fields.Integer(
        config_parameter="installment.delay_penalty_process"
    )
    nid = fields.Boolean(config_parameter="installment.nid", default=False)
    salary_components = fields.Boolean(
        config_parameter="installment.salary_components", default=False
    )
    bank_statement = fields.Boolean(
        config_parameter="installment.bank_statement", default=False
    )
    bank_rate_letter = fields.Boolean(
        config_parameter="installment.bank_rate_letter", default=False
    )
    rental_contract = fields.Boolean(
        config_parameter="installment.rental_contract", default=False
    )
    owership_contract = fields.Boolean(
        config_parameter="installment.owership_contract", default=False
    )
