# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    timer_active = fields.Boolean()
    timer_start_time = fields.Datetime()
    max_work_hours_per_day = fields.Float(string='Maximum Work Hours', default=8.0)
