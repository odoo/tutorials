from odoo import _, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def open_warranty_wizard(self):
        print("inside the wizard button")
        self.ensure_one()
        return{
            'name': _("Warranty"),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.warranty',
            'view_mode': 'form',
            'target': 'new',
        }
