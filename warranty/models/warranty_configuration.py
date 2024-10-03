from odoo import fields, models


class WarrantyConfiguration(models.Model):
    _name = "storewarranty.configuration"
    _description = "model to store warranty configuration"

    name = fields.Char(string="Name")
    product_id = fields.Many2one("product.product", required=True)
    percentage = fields.Float(string="Percentage", required=True)
    period = fields.Integer(string="year", required=True)
