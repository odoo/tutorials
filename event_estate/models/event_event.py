from odoo import models, fields


class Event(models.Model):
    _inherit = 'event.event'

    property_id = fields.Many2one(
        'estate.property',
        string="Property"
    )
