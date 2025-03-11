from odoo import fields, models


class estateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        result = super().action_set_sold_property()

        self.env["account.move"].create(
            {
                "partner_id": self.buyer_id.id,
                "move_type": "out_invoice",
                "journal_id": self.env["account.journal"]
                .search([("type", "=", "sale")], limit=1)
                .id,
            }
        )
        return result
