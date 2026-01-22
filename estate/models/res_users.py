from odoo import api, fields, models


class EstatePropertyUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', 'seller_id')
    name = fields.Char()

    prices = fields.One2many(
        'estate.property', 'seller_id')
    total_unsold_value = fields.Float(
        compute='_compute_total_unsold_value')

    @api.depends('prices.expected_price', 'prices.state')
    def _compute_total_unsold_value(self):
        for record in self:
            unsold_prices = record.prices.filtered(lambda p: p.state != 'sold')
            record.total_unsold_value = (
                sum(unsold_prices.mapped('expected_price')
                    ) if unsold_prices else 0.0
            )
