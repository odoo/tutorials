from odoo import models,fields

class WarrantyConfigurations(models.Model):
    _name = "warranty.configurations"
    _description = "Add warranty"

    name = fields.Char()
    product_id = fields.Many2one("product.template",string="Product")
    percentage = fields.Float()
