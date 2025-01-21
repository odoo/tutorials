from odoo import fields, models


class EventTicketInherit(models.Model):
    _inherit = "event.event.ticket"

    tickets_per_registration = fields.Integer(
        string="Tickets per Registration",
        help="Number of tickets per registration. 0 means unlimited.",
    )
