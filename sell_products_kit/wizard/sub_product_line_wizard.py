from odoo import fields, models


class SubProductLineWizard(models.TransientModel):
    _name = "sub.product.line.wizard"
    _description = "Sub Product Line wizard"

    parent_wizard = fields.Many2one("sub.product.wizard")
    product_id = fields.Many2one("product.product", required=True)
    price = fields.Float(default=0)
    quantity = fields.Integer(default=0)
