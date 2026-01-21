from odoo import fields, models


class EstatePropertyInvestor(models.Model):
    _name = 'estate.property.investor'
    _description = 'Property Investor'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner',required=True, ondelete='cascade')
