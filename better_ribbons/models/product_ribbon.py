from odoo import fields, models


class ProductRibbon(models.Model):
    _inherit = 'product.ribbon'
    _order = 'sequence asc, create_date asc'

    style = fields.Selection(
        [('ribbon', 'Ribbon'), ('tag', 'Badge')],
        string='Style',
        required=True,
        default='ribbon',
    )

    assign = fields.Selection(
        [
            ('manually', 'Manually'),
            ('sale', 'Sale'),
            ('out_of_stock', 'Out of Stock'),
            ('new', 'New'),
        ],
        string='Assign',
        required=True,
        default='manually',
    )

    new_until = fields.Integer(default=30, help='Days to consider a product as new')
    sequence = fields.Integer(default=10, help='Sequence to prioritize ribbons')

    def _get_position_class(self):
        return f'o_{self.style}_{self.position}'
