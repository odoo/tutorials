from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_unique_id = fields.Char("Unique ID", unique=True)
    import_histry_ids = fields.One2many('product.import.histry', 'product_id', string="Import Histry")
