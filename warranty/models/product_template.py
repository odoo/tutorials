from odoo import models,fields

class ProductTemplate(models.Model):
    _inherit = "product.template"

    warranty = fields.Boolean(default=False, string="Is warranty available")
    