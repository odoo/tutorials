from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class list_product(models.TransientModel):
    _name = "product.list.product"
    _description = "product.list.product"

    product_id = fields.Many2one(
        "product.product",
        string="product",
        required=True,
    )
    qty = fields.Integer(default=1)
    add_product_id = fields.Many2one("product.add.product", string="add_warranty")
    order_line_id = fields.Integer(required=True)
    price = fields.Integer()
