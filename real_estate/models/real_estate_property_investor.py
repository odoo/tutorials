from odoo import models, fields


class RealEstatePropertyInvestor(models.Model):
    _name = 'real.estate.property.investor'
    _description = 'Real Estate Property Investor'

    partner_id = fields.Many2one('res.partner')

# class RealEstatePropertyInvestor(models.Model):
#     _name = 'real.estate.property.investor'
#     _description = 'Real Estate Property Investor'
#     _inherits = {'res.partner': 'partner_id'}
#
#     partner_id = fields.Many2one('res.partner', required=True, ondelete='cascade')
