from odoo import fields, models


class InstallmentModel(models.TransientModel):
    _inherit = "res.config.settings"

    max_duration = fields.Float(
        string="Max Duration", config_parameter="installment.max_duration"
    )
    down_payment_perc = fields.Integer(
        string="Down Payment Percentage",
        config_parameter="installment.down_payment_perc",
    )
    annual_rate_perc = fields.Integer(
        string="Annual Rate Percentage", config_parameter="installment.annual_rate_perc"
    )
    administ_exp = fields.Integer(
        string="Administrative Expenses Percentage",
        config_parameter="installment.administ_exp",
    )
    delay_panalty_perc = fields.Integer(
        string="Delay Penalty Percentage",
        config_parameter="installment.delay_panalty_perc",
    )
    delay_panalty_process = fields.Float(
        string="Max Duration", config_parameter="installment.delay_panalty_process"
    )
    nid = fields.Boolean("Nid", config_parameter="installment.nid")
    salary_component = fields.Boolean(
        "Salary Component", config_parameter="installment.salary_component"
    )
    bank_statement = fields.Boolean(
        "Bank Statement", config_parameter="installment.bank_statement"
    )
    bank_rate_letter = fields.Boolean(
        "Bank Rate Letter", config_parameter="installment.bank_rate_letter"
    )
    rental_contract = fields.Boolean(
        "Rental Contract", config_parameter="installment.rental_contract"
    )
    owner_contract = fields.Boolean(
        "Ownership Contract", config_parameter="installment.owner_contract"
    )
