from odoo import fields, models


class OrderLineWizardLine(models.TransientModel):
    _name = "order.line.wizard"
    _description = "order line wizard line"

    wizard_id = fields.Many2one("order.wizard", string="Wizard")
    price = fields.Float(string="Price", store=True)
    product_template_id = fields.Many2one("product.template", string="Product")
    order_line_id = fields.Many2one("sale.order.line", string="Order Line")
    include_for_division = fields.Boolean(
        "Include orderline for division", default="true"
    )
