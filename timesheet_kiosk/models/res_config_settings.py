from odoo import  fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _name = 'res.config.settings'

    timesheet_kiosk_max_hours = fields.Float(
        string='Max Allowed Timesheet Hours from Kiosk',
        config_parameter='timesheet_kiosk.timesheet_kiosk_max_hours',
        default=8.0,
    )

    timesheet_kiosk_email_template_id = fields.Many2one(
        'mail.template',
        string='Email Template for PM',
        config_parameter='timesheet_kiosk.timesheet_kiosk_email_template_id',
    )