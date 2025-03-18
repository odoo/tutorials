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
    show_period = fields.Integer(default=30)

    def _get_position_class(self):
        if self.style == 'ribbon':
            return 'o_ribbon_left' if self.position == 'left' else 'o_ribbon_right'
        else:  # self.style == 'badge'
            return 'o_tag_left' if self.position == 'left' else 'o_tag_right'
