from odoo import fields, models


class PropertyPlan(models.Model):
    _inherit = "product.template"

    sec_uom_id = fields.Many2one(
        "uom.uom",
        "Second Unit of Measure",
        help="Second unit of measure used for all stock operations.",
    )
