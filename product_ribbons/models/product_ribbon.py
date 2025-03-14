from odoo import fields, models


class ProductRibbon(models.Model):
    _inherit = "product.ribbon"

    style = fields.Selection(
        [("badge", "Badge"), ("ribbon", "Ribbon")],
        string="Style",
        default="ribbon",
        required=True,
    )
    assign = fields.Selection(
        [
            ("manual", "Manual"),
            ("sale", "Sale"),
            ("out_of_stock", "Out of Stock"),
            ("new", "New"),
        ],
        string="Assign",
        default="manual",
        required=True,
    )
    show_after_days = fields.Integer(default=30)
