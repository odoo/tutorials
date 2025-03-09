from odoo import api, fields, models

class SubProductLineWizard(models.TransientModel):
    _name = "sub.product.line.wizard"
    _description = "Sub Product Line Wizard"

    sub_product_wizard_id = fields.Many2one("sub.product.wizard", required=True, ondelete="cascade")
    product_id = fields.Many2one("product.product", required=True)
    quantity = fields.Float(string="Quantity", default=1.0)
    price = fields.Float(string="Price")
    order_line_id = fields.Many2one("sale.order.line")
