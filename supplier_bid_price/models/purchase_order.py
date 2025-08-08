from odoo import models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def _send_bid_update_email(self, mail_values):
        if not mail_values:
            return
        template = self.env.ref('supplier_bid_price.email_template_supplier_bid_update').sudo()
        if template:
            email_ctx = {
                'mail_values': mail_values
            }
            template.with_context(**email_ctx).send_mail(self.id, force_send=True)
