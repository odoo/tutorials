from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    deposit_required = fields.Boolean(help="Enable if this product requires deposit.")
    deposit_amount = fields.Float(help="This specifies deposit for 1 unit of this product.")
