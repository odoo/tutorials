from odoo import models, fields, api, _


class PackagingOrder(models.Model):
    _name = 'packaging.order'
    _description = 'Packaging Order'

    name = fields.Char(
        string='Order Reference',
        required=True,
        copy=False,
        readonly=True,
        default='New'
    )

    production_order = fields.Many2one(
        'mrp.production',
        string='Production Order'
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], default='draft'
    )

    oreration_id = fields.Many2one(
        'res.users',
        string='Packing Operator'
    )

    def action_start(self):
        self.state = 'in_progress'

    def action_done(self):
        if any(line.packed_qty < line.quantity for line in self.line_ids):
            raise ValueError(_('Not all items are packed yet!'))
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancelled'

    class PackagingLine(models.Model):
        _name = 'packaging.line',
        _description = 'Packaging Line'

        order_id = fields.Many2one('packaging.order', required=True, ondeleted='cascade')
        product_id = fields.Many2one('product.product', string='Product', required=True)
        quantity = fields.Float(string='Quatity to pack')
        packed_qty = fields.Float(string='Packed Quantity', default=0.0)            