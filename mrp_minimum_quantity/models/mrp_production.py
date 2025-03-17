# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, models
from odoo.exceptions import ValidationError


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    @api.onchange("product_qty")
    def _onchange_product_qty(self):
        if not self.bom_id:
            return
        if self.product_qty < self.bom_id.product_min_qty:
            message = _("Minimum Quantity cannot be lower than Quantity.")
            if self.env.user.has_group("mrp.group_mrp_manager"):
                return {
                    "warning": {
                        "title": _("Warning"),
                        "message": message,
                    }
                }
            else:
                raise ValidationError(message=message)
