from odoo import models, fields, api

class EventEvent(models.Model):
    
   
    _inherit = 'event.event.ticket'

    max_tickets_per_order = fields.Integer(
        string="Max Tickets per Order",
        readonly=True,  # Optional: Make it read-only
    )
