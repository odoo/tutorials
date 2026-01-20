from odoo import fields, models, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        'real.estate',
        'salesperson_id',
        string='Assigned Properties'
    )
    total_unsold = fields.Float(
        string="Total Unsold Value",
        compute="_compute_total_unsold_value",
        store=True
    )

    @api.depends('property_ids.stage', 'property_ids.expected_price')
    def _compute_total_unsold_value(self):
        sum_unsold = dict(self.env['real.estate']._read_group(
            domain=[('salesperson_id', '=', self.ids),
                ('stage', '!=', 'sold')],
            groupby=['salesperson_id'],
            aggregates=['expected_price:sum'],
        ))
        for record in self:
            record.total_unsold = sum_unsold.get(record, 0.0)
