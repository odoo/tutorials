from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    modular_type_ids = fields.Many2many("modular.type", string="Module Types")
