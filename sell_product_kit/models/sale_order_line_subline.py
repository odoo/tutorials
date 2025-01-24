from odoo import fields, models

class SaleOrderLineSubline(models.Model):
    _name= "sale.order.line.subline"
    
    sale_order_line_id=fields.Many2one(comodel_name='sale.order.line', ondelete="cascade")
    product_id=fields.Many2one(comodel_name="product.product")
    quantity=fields.Integer()
    price=fields.Float()
