from odoo import models, fields


class KitWizardLine(models.TransientModel):
    _name = "kit.wizard.line"
    _description = "Kit Wizard Line"

    wizard_id = fields.Many2one("product.kit.wizard")
    product_id = fields.Many2one("product.product", readonly=True)
    quantity = fields.Float()
    price = fields.Float()
    # existing_line_id = fields.Many2one("sale.order.line", string="Existing Product order line")
