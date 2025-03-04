from odoo import fields, models


class SubProductsWizardLine(models.TransientModel):
    _name = "subproducts.wizard.line"
    _description = "Wizard Line for Sub Products"

    wizard_id = fields.Many2one(
        "subproducts.wizard", string="Wizard", required=True, ondelete="cascade"
    )
    product_id = fields.Many2one("product.product", string="Sub Product")
    quantity = fields.Float(string="Quantity", required=True)
    price = fields.Float(string="Price", required=True)
