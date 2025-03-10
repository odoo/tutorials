from odoo import models,fields

class WarrantyConfiguration(models.Model):
    _name = "warranty.configuration"
    _description = "Add warranty"

    name = fields.Char(required=True,string="Name")
    product_id = fields.Many2one("product.template",string="Product")
    percentage = fields.Float()
