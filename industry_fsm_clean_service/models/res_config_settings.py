# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    automated_client_notification = fields.Boolean(
        string="Automated Client Notifications",
        help="Enable automated email reminders for clients before scheduled service.",
        config_parameter='fsm_reminder.automated_client_notification',
    )
    days_prior = fields.Integer(
        string="Day(s) Prior",
        help="Specify how many days before the scheduled service the reminder should be sent.",
        config_parameter='fsm_reminder.days_prior',
    )
    email_template_id = fields.Many2one(
        comodel_name='mail.template',
        string="Email Template",
        domain=[('model', '=', 'project.task')],
        help="Choose an email template for the reminder.",
        config_parameter='fsm_reminder.email_template_id',
    )
