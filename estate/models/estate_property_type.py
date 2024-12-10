from odoo import models, fields
class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'
    name = fields.Char(string="Property Type", required=True)
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer")
    seller_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
