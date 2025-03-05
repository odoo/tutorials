from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    modular_type_ids = fields.Many2many(
        comodel_name="modular.type",
        relation="product_modular_type_rel",
        column1="product_id",
        column2="modular_type_id",
        string="Modular Types",
        readonly=False
    )
