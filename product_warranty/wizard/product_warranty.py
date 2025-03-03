from odoo import Command,_, api, fields, models


class ProductWarranty(models.TransientModel):
    _name = 'product.warranty'
    _description = "Add warranty"

    sale_order_id = fields.Many2one(
        'sale.order',
        string="Order",
        required=True,
    )
    warranty_line_ids = fields.One2many(
        'warranty.line',
        'product_warranty_id',
        string="Warranty lines",
        compute='_compute_warranty_line_ids',
        store=True,
    )

    @api.depends('sale_order_id')
    def _compute_warranty_line_ids(self):
        """ Compute warranty lines dynamically based on the sale order. """
        for wizard in self:
            wizard.warranty_line_ids = [
                Command.create({
                    'sale_order_line_id': line.id,
                })
                for line in wizard.sale_order_id.order_line
                if line.product_template_id and line.product_template_id.is_warranty
            ]

    def action_add_warranty(self):
        product_warranty = self.env.ref('product_warranty.extended_warranty_product', raise_if_not_found=False)
        warranty_line_vals = [
            {
                'order_id': self.sale_order_id.id,
                'product_id': product_warranty and product_warranty.id,
                'name': self.env._("Extended Warranty End Date: %s", line.end_date.strftime('%Y-%m-%d')),
                'product_uom_qty': line.sale_order_line_id.product_uom_qty,
                'price_unit': (
                    (line.product_warranty_config_id.percentage / 100) *
                    line.sale_order_line_id.price_unit
                ),
                'linked_line_id': line.sale_order_line_id.id,
            }
            for line in self.warranty_line_ids if line.product_warranty_config_id
        ]
        if warranty_line_vals:
            self.env['sale.order.line'].create(warranty_line_vals)
