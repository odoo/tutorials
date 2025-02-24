from odoo import fields, models


class Warranty(models.Model):
    _name = "warranty"
    _description = "Warranty Configuration"

    name = fields.Char("Name", required=True)
    product_id = fields.Many2one("product.template", string="Product", required=True)
    percentage = fields.Float("Percentage", required=True)
