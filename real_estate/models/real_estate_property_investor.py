from odoo import models, fields


class RealEstatePropertyInvestor(models.Model):
    _name = 'real.estate.property.investor'
    _description = 'Real Estate Property Investor'

    name = fields.Many2one('res.partner')
