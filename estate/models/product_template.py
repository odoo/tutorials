from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    service_manual_delivery = fields.Boolean(
        string="Manual Delivered Service",
        compute="_compute_service_manual_delivery",
        store=True
    )

    @api.depends('type', 'service_type', 'invoice_policy')
    def _compute_service_manual_delivery(self):
        for product in self:
            product.service_manual_delivery = (
                product.type == 'service'
                and product.service_type == 'manual'
                and product.invoice_policy == 'delivery'
            )
