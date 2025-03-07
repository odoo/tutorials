from odoo import Command, _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_kit = fields.Boolean(string="Is Kit", related='product_id.is_kit')
    kit_component_ids = fields.One2many(
        comodel_name='product.kit.component',
        inverse_name='parent_order_line_id',
        string="Kit Components",
        compute="_compute_sub_products",
        store=True,
        help="List of sub products"
    )
    is_kit_component = fields.Boolean(string="Is Kit Component?")
    kit_parent_line_id = fields.Many2one(
        comodel_name='sale.order.line',
        string="Parent Kit Line",
        help="Refrence to the main kit product's sale order line"
    )

    def open_kit_wizard(self):
        self.ensure_one()
        return self.env['product.kit'].with_context(
            default_sale_order_line_id=self.id,
        )._get_records_action(name=_("Product Kit Wizard"), target='new')

    @api.depends('product_id')
    def _compute_sub_products(self):
        """
        Computes the sub-products (kit components) for a sale order line.
        It retrieves the sub-products linked to the main product and updates
        the `kit_component_ids` field accordingly.
        """
        for line in self:
            for sub_product in line.product_id.product_tmpl_id.sub_product_ids:
                if sub_product not in line.kit_component_ids.kit_component_id:
                    line.kit_component_ids = [
                        Command.create({
                            'parent_order_line_id': line.id,
                            'kit_component_id': sub_product.id,
                            'price': sub_product.lst_price,
                        })
                    ]

    @api.ondelete(at_uninstall=False)
    def _delete_sub_products(self):
        """
        Ensures that when a kit product is deleted from a sale order,
        all its linked kit component lines are also removed.
        """
        lines_with_kit = self.filtered(lambda l: l.is_kit)
        if lines_with_kit:
            self.env['sale.order.line'].search([
                ('order_id', 'in', lines_with_kit.order_id.ids),
                ('kit_parent_line_id', 'in', lines_with_kit.ids)
            ]).unlink()

    def write(self, vals):
        """
        Prevents manual modification of key fields (`product_id`, `product_uom_qty`, `price_unit`)
        for sub-products (components of a kit) to maintain data integrity.
        """
        if (
            any(line.is_kit_component for line in self)
            and any(field in vals for field in {'product_id', 'product_uom_qty',
            'price_unit'})
        ):
            raise ValidationError("Subproduct of a kit cannot be modified manually")
        return super(SaleOrderLine, self).write(vals)
