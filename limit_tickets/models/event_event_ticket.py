from odoo import fields, models


class EventEventTicket(models.Model):
    _inherit = "event.event.ticket"

    max_tickets_register = fields.Integer(
        string="Max tickets per registration",
        default=9,
        help="Limits the maximum number of tickets per registration",
    )

    _sql_constraints = [
        (
            "check_max_tickets_register",
            "CHECK(max_tickets_register > 0 AND max_tickets_register < 10)",
            "The maximum tickets per registration must be between 1-9.",
        )
    ]
