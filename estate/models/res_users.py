from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        'estate.property',
        'seller_id',
    )
    total_expected = fields.Float(compute="_compute_total_expected")

    @api.depends('property_ids.expected_price', 'property_ids.state')
    def _compute_total_expected(self):
        sum_expected = dict(self.env['estate.property']._read_group(
            domain=[('state', '!=', 'sold'), ('seller_id', 'in', self.ids)],
            aggregates=['expected_price:sum'],
            groupby=['seller_id']
        ))
        for record in self:
            record.total_expected = sum_expected.get(record, 0.0)
        # for record in self:
        #     validate_property = record.property_ids.filtered(
        #         lambda p: p.state != 'sold'
        #     )
        #     record.total_expected = sum(validate_property.mapped('expected_price'))
