# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    max_work_hours_per_day = fields.Float(
        string="Max Work Hours per Day",
        config_parameter="time_tracking_kiosk.max_work_hours_per_day",
        help="Maximum allowed work hours per day for employees using the kiosk.",
    )

    pm_notification_template_id = fields.Many2one(
        comodel_name="mail.template",
        string="PM Notification Email Template",
        domain=[("model", "=", "account.analytic.line")],
        config_parameter="time_tracking_kiosk.pm_notification_template_id",
        help="Select the email template to notify project managers.",
    )
