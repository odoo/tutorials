from odoo import models, fields

class EventTicket(models.Model):
    _inherit = "event.event.ticket"

    max_tickets_per_registration = fields.Integer(string="Max Tickets per Registration", help="Define the maximum number of tickets that can be booked per registration.")
