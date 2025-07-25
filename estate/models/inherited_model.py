from odoo import fields, models

class InheritedModel(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(comodel_name="estate_property", inverse_name = "salesperson", domain = [('state', 'in', ['New', 'Offer Received'])])

