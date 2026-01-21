from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        'estate.property',
        'seller_id',
        string="Assigned Properties",
    )

    total_expected = fields.Float(string="Total Expected Price", compute="_compute_total_expected")

    @api.depends('property_ids.expected_price', 'property_ids.state')
    def _compute_total_expected(self):
        for record in self:
            result = record.property_ids._read_group(
                domain=[
                    ('seller_id', '=', record.id),
                    ('state', '!=', 'sold'),
                ],
                aggregates=['expected_price:sum'],
                groupby=[]
            )
            record.total_expected = result[0][0] if result else 0.0
