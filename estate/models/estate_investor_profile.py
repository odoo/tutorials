from odoo import fields, models


class EstatePropertyInvestor(models.Model):
    _name = 'estate.property.investor'
    _description = 'Estate Property investor'

    name = fields.Many2one('res.partner', string="investor")
    property_ids = fields.One2many('estate.property', 'buyer_ids')
