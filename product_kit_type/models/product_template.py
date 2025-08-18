from odoo import models, fields, api


class InheritedProductTemplate(models.Model):
    _inherit = "product.template"

    is_kit = fields.Boolean("Is kit?")
    sub_products = fields.Many2many("product.product", string="Sub Products")

    @api.onchange("is_kit")
    def _onchange_is_kit(self):
        if not self.is_kit:
            self.sub_products = None
