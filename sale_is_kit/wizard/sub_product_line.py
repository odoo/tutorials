from odoo import fields, models


class SubProductLine(models.TransientModel):
    _name = 'sub.product.line'


    product_id = fields.Many2one(comodel_name='product.product', required=True, ondelete='cascade')
    quantity = fields.Integer(string="Quantity", required=True, default=1)
    price_unit = fields.Float(string="Unit Price", required=True)
    sub_product_wizard_id = fields.Many2one('sub.product.wizard',required=True, ondelete='cascade')

