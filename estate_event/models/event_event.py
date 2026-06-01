from odoo import models, fields


class EventEvent(models.Model):
    _inherit = "event.event"

    property_id = fields.Many2one("estate.property", string="Property")
