from odoo import api, fields, models


class EstatePropertyUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', 'seller_id')
    name = fields.Char()

    total_unsold_value = fields.Float(
        compute='_compute_total_unsold_value')

    @api.depends('property_ids.expected_price', 'property_ids.state')
    def _compute_total_unsold_value(self):
        for record in self:
            unsold_prices = record.property_ids.filtered(
                lambda p: p.state != 'sold')
            record.total_unsold_value = (
                sum(unsold_prices.mapped('expected_price')
                    ) if unsold_prices else 0.0
            )
