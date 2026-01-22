from odoo import fields, models, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', 'partner_id')
    unsold_cost = fields.Integer(compute='_compute_price')

    @api.depends('property_ids.state', 'property_ids.expected_price')
    def _compute_price(self):
        result = dict(self.env['estate.property']._read_group(
            [('partner_id', '=', self.ids), ('state', '!=', 'sold')],
            ['partner_id'],
            ['expected_price:sum']
        ))
        for record in self:
            record.unsold_cost = result.get(record, 0.0)

# Task 2: Compute total unsold value on res.partner:
# Sum of expected_price
# From estate.property
# State ≠ sold
