from odoo import fields, models

class WarrantyConfiguration(models.Model):
    _name = "warranty.configuration"
    _description = "Add warranty for products"

    name = fields.Char(string = "Name", required = True)
    duration = fields.Integer(string = "Duration (in Years)")
    percentage = fields.Float(string = "Percentage", required = True)
    product_id = fields.Many2one('product.template', string = "Product", ondelete="cascade", required=True)
