from odoo import models


class EstatePropert(models.Model):
    _inherit = "estate.property"

    def action_set_property_sold(self):
        self.env["account.move"].create(
            {"partner_id": self.partner_id.id, "move_type": "out_invoice"}
        )
        return super().action_set_property_sold()
