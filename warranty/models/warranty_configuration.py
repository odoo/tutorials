from odoo import fields, models

class WarrantyConfiguration(models.Model):
    _name = "warranty.configuration"
    _description = "warranty model for products"

    name = fields.Char(required=True, string="Name")
    product_id = fields.Many2one(comodel_name="product.template",  string="Product")
    percentage = fields.Float(DecimalPrecision=2, default=0.0, required=True)
    duration = fields.Integer(string="Duration (Years)", required=True, default=0)  


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_warranty_available = fields.Boolean(default=False, string="is warranty available")
    
class SaleOrder(models.Model):
    _inherit = "sale.order.line"

    warranty_id = fields.Many2one('sale.order.line', string="Warranty For", help="The original order line associated with this warranty", ondelete="cascade")
