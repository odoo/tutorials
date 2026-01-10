from odoo import fields, models


class productTemplate(models.Model):
    _inherit = "product.template"

    modular_type_ids = fields.Many2many(
        "modular.type", help="Help to give modular type to product"
    )
