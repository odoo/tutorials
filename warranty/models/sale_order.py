from odoo import _, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def open_warranty_wizard(self):
        self.ensure_one()
        return{
            'name': _("Warranty"),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.warranty',
            'view_mode': 'form',
            'target': 'new',
            'context': {'sale_order_id': self.id}
        }
