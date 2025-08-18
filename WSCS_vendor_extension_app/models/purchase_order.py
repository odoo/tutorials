from odoo import models, fields, api
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.model
    def create(self, vals):
        partner = self.env["res.partner"].browse(vals.get("partner_id"))
        vendor_status = partner.vendor_status_id
        if vendor_status.prevent_po_creation == "yes":
            raise UserError("This vendor is not allowed to create a Purchase Order.")
        elif vendor_status.prevent_po_creation == "alert":
            raise UserError(
                "PO creation is restricted for this vendor and needs manual approval."
            )
        order = super().create(vals)
        next_status = self.env["vendor.status"].search(
            [("sequence", ">", vendor_status.sequence)], order="sequence asc", limit=1
        )
        if next_status.status_change_type == "automatic":
            if next_status:
                partner.vendor_status_id = next_status.id
        return order
