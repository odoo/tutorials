from odoo import fields, models


class EventTicket(models.Model):
    _inherit = "event.event"

    set_max_ticket = fields.Integer(
        string="Set Max Registration Limit",
        default=10,
        help="Limit number of tickets per registration",
    )
