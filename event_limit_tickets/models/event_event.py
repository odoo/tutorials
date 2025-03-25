from odoo import fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    max_tickets_per_registration = fields.Integer(string="Max Tickets", default=10)
