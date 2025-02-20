from odoo import models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_status_sold(self):
        self.env['account.move'].create(
            {
                'partner_id': self.partner_id,
                'move_type': 'out_invoice',

            }
        )
        return super().action_set_status_sold()
