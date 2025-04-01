# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class WarrantyConfiguration(models.Model):
    _name = 'warranty.configuration'
    _sql_constraints = [
        ('check_positive_value_validity', 'CHECK(validity>0)',
         "Warranty's validity must be positive"),
        ('check_positive_value_percentage', 'CHECK(percentage>0)',
         "Warranty's percentage must be positive")
    ]

    name = fields.Char(string="Name", required=True)
    validity = fields.Integer(string="Valid till(in Year)", required=True)
    product_id = fields.Many2one(comodel_name='product.product', string="Product", required=True)
    percentage = fields.Float(string="Percentage", required=True)
