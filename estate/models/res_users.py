from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', 'user_id')
    unsold_value = fields.Float(compute='_compute_unsold_value')

    @api.depends('property_ids.expected_price', 'property_ids.state', 'property_ids.user_id')
    def _compute_unsold_value(self):
        sum_unsold_value = dict(self.env['estate.property']._read_group(domain=[('state', '!=', 'sold'), (
            'user_id', 'in', self.ids)], aggregates=['expected_price:sum'], groupby=['user_id']))
        for record in self:
            record.unsold_value = sum_unsold_value.get(record)
