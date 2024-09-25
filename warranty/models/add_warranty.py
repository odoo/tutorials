from odoo import fields, models


class AddWarranty(models.Model):
    _name = "add.warranty"
    _description = "Warranty Configuration"

    name = fields.Char(string="Name", required=True)
    percentage = fields.Float(string="Percentage")
    period = fields.Integer(string="Period")
    product_id = fields.Many2one("product.product", string="Product")
