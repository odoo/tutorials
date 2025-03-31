from odoo import fields, models

class InheritedResUser(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many('real.estate.property', 'salesperson_id', string = 'Property', domain = [('status', 'in', ['new', 'offer_received'])])
