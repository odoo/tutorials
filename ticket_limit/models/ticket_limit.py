from odoo import models, fields, api

class EventTicket(models.Model):
    _inherit = "event.event.ticket"

    tickets_per_registration = fields.Integer(string="Tickets per Registration", default=1)
