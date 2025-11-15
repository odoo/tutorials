from odoo import fields, models


class SubproductLineWizard(models.TransientModel):
    _name = "subproduct.line.wizard"
    _description = "Subproduct line wizard view"

    wizard_id = fields.Many2one(comodel_name="product.kit.wizard", ondelete="cascade")
    product_id = fields.Many2one(comodel_name="product.product")
    quantity = fields.Float(string="Quantity", required=True, default=1.0)
    unit_price = fields.Float(string="Price", required=True)
