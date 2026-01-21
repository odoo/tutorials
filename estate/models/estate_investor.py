from odoo import fields, models


class EstateInvestor(models.Model):
    _name = "estate.investor"
    _description = "investor details"
    _rec_name = 'id'

    name = fields.Many2one('res.partner')
