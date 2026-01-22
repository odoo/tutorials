from odoo import fields, models


class EstateInvestor(models.Model):
    _name = 'estate.investor'
    _description = 'Estate Investor'
    # _inherit = 'res.partner'

    name = fields.Many2one('res.partner')
