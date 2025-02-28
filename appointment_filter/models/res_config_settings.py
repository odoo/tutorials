from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    step_value = fields.Integer(
        string="Appointments Per Page",
        config_parameter="appointment_filter.step_value",
        default=12
    )
