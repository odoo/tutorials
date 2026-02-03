from odoo import api, fields, models


class InheritedResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', 'salesman_id')
    total_unsold_value = fields.Float(compute='_compute_total_unsold_value')
    estate_property_ids = fields.One2many('estate.property', 'salesman_id')

    @api.depends('estate_property_ids.expected_price')
    def _compute_total_unsold_value(self):
        result = dict(
            self.env['estate.property']._read_group(
                [('salesman_id', 'in', self.ids), ('state', '!=', 'sold')],
                ['salesman_id'],
                ['expected_price:sum'],
            )
        )
        for record in self:
            record.total_unsold_value = result.get(record)
