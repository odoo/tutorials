# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EventTemplateTicket(models.Model):
    _inherit = "event.type.ticket"

    max_tickets_per_registration = fields.Integer(
        string="Max Tickets Per Registration",
        default=9,
        help="Define the maximum number of tickets allowed per registration. Between 1-9"
    )

    _sql_constraints = [
        (
            "check_max_tickets_per_registration",
            "CHECK(max_tickets_per_registration > 0 AND max_tickets_per_registration < 10)",
            "The maximum tickets per registration must be between 1-9."
        )
    ]
