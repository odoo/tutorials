from odoo import fields, models


class SaleOrderLineModularValue(models.Model):
    _name = "sale.order.line.modular.value"
    _description = "Sale Order Line Modular Value"

    sale_line_id = fields.Many2one(
        "sale.order.line",
        string="Sale Order Line",
        required=True,
        ondelete="cascade",
    )

    modular_type_id = fields.Many2one(
        "modular.type",
        string="Modular Type",
        required=True,
    )

    value = fields.Float(
        string="Value",
        default=1.0,
        required=True,
    )
