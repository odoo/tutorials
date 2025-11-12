from odoo import models, fields
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    warranty_id = fields.Boolean(default=False)



