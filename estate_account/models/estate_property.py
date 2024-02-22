from odoo import models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_to_sold(self):
        for property in self:
            self.env['account.move'].create(
                {
                    'partner_id': property.buyer_id.id,
                    'move_type': 'out_invoice'
                })
        return super().action_set_to_sold()
