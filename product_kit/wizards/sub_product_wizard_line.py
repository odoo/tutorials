from odoo import fields, models


class SubproductWizardLine(models.TransientModel):
    _name = 'subproduct.line'
    _description = 'Sub-product Wizard Line'

    subproduct_line_id = fields.Many2one('subproduct')
    product_id = fields.Many2one('product.product')
    sub_product_name = fields.Char(string="Product Name")
    quantity = fields.Integer(string="Quantity")
    unit_price = fields.Float(string="Unit Price")
