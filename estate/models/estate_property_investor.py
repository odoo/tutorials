from odoo import fields, models


class EstateInvestor(models.Model):
    _name = 'estate.investor'
    _description = "Estate Investor"

    name = fields.Many2one('res.partner')
    # a = fields.Char("AA")
    # city = fields.Char(compute='_compute_city')

    # def _compute_city(self):
    #     for record in self:
    #         record.city = record.name.city if record.name else ''
