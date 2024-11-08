from odoo import fields, models

class SubProductAddLine(models.TransientModel):
    _name = "add.sub.product.line"

    product_id = fields.Many2one('product.product', string='Sub Product')
    sub_product_id = fields.Many2one("add.sub.product.wizard", string="Wizard Reference")
    quantity = fields.Float(string='Quantity')
    price = fields.Float(string='Price')
