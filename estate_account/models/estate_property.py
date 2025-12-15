from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self) -> bool:
        percent_description = "6 percent of selling price"
        admin_fee_description = "Administrative fees"
        # Note: does not work if fiscal localization is not set
        for record in self:
            account_move = {
                "partner_id": record.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create({"name": percent_description, "quantity": 1, "price_unit": 0.06 * record.selling_price}),
                    Command.create({"name": admin_fee_description, "quantity": 1, "price_unit": 100.0}),
                ],
            }
            self.env["account.move"].create(account_move)
        return super().action_set_sold()
