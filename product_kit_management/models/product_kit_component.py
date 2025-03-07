from odoo import fields, models


class ProductKitComponent(models.Model):
    _name = 'product.kit.component'
    _description = "Product Kit Component"

    parent_order_line_id = fields.Many2one(
        comodel_name="sale.order.line",
        help="Refrence to the sale order line this kit component belongs to."
    )
    kit_component_id = fields.Many2one(
        comodel_name="product.product", string="Sub Product",
        help="sub-product that is part of kit"
    )
    kit_qty = fields.Integer(
        string="Quantity",
        required=True,
        default=1,
        store=True
    )
    price = fields.Float(string="Price", required=True)
