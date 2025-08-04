# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta
from odoo import fields, models

class ProjectTask(models.Model):
    _inherit = 'project.task'
    _order = 'sequence asc'

    fsm_reminder_sent = fields.Boolean(
        string="FSM Reminder Sent",
        default=False,
        help="Indicates whether a reminder email has been sent for this task.",
    )

    def _send_fsm_task_reminders(self):
        """Send reminders to clients X days before the scheduled service date, only if the task is in 'Planned' stage."""
        config = self.env['ir.config_parameter'].sudo()
        automated_notifications = (config.get_param('fsm_reminder.automated_client_notification', default='False') == 'True')
        days_prior = int(config.get_param('fsm_reminder.days_prior', default='0'))
        email_template_id = int(config.get_param('fsm_reminder.email_template_id', default='0'))

        if not automated_notifications or not email_template_id or days_prior <= 0:
            return

        email_template = self.env['mail.template'].browse(email_template_id)
        if not email_template.exists():
            return

        reminder_date = fields.Date.today() + timedelta(days=days_prior)
        planned_stage_id = self.env.ref('industry_fsm.planning_project_stage_1').id
        if not planned_stage_id:
            return

        tasks = self.env['project.task'].search([
            ('planned_date_begin', '>=', datetime.combine(reminder_date, datetime.min.time())),
            ('planned_date_begin', '<', datetime.combine(reminder_date, datetime.max.time())),
            ('stage_id', '=', planned_stage_id),
            ('partner_id', '!=', False),
            ('name', 'ilike', 'Cleaning Services'),
            ('fsm_reminder_sent', '=', False),
        ])
        for task in tasks:
            email_template.send_mail(task.id, force_send=True)
            task.fsm_reminder_sent = True
            task.message_post(
                body=(
                    f"Reminder email sent to {task.partner_id.name} for scheduled service!"
                ),
                subtype_xmlid='mail.mt_note',
            )
