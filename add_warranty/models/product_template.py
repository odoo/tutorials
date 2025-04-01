from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_warranty = fields.Boolean(string = "Is warranty available", default = False)