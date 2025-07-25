from odoo import fields, models

class InheritedModel(models.Model):
    _inherit = "res.users"
    _description = "Res Users Inherited model"
    property_ids = fields.One2many(comodel_name="estate_property", inverse_name = "salesperson", domain = [('state', 'in', ['New', 'Offer Received'])])

