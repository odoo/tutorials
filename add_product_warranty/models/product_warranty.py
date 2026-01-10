from odoo import fields, models


class productWarranty(models.Model):
    _name = "product.warranty"
    _description = "Product Warranty"

    name = fields.Char(string="Name", required=True)
    percentage = fields.Float(string="Percentage", required=True)
    validity_year = fields.Integer(string="Validity Year")
