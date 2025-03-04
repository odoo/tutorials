from odoo import fields, models


class WarrantyConfiguration(models.Model):
    _name ="warranty.configuration"
    _description = "Warranty Configuration model"

    name=fields.Char(string="Name")
    product_id= fields.Many2one(comodel_name='product.template',string="Product",required=True)
    percentage = fields.Float(string="Percentage",required=True)
    warranty_period=fields.Integer(string="Warranty Period", required=True)
