from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    uom_category_id = fields.Many2one(
        related="uom_id.category_id", string="UOM Category", readonly=True, store=True
    )

    pos_second_uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="POS second UOM",
        domain="[('category_id', '=', uom_category_id)]",
        store=True,
    )
