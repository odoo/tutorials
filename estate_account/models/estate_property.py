from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self) -> bool:
        # Call the action on the base model first to ensure validation is done (e.g. one accepted offer)
        result = super().action_set_sold()

        percent_description = "6 percent of selling price"
        admin_fee_description = "Administrative fees"
        account_moves = []
        for record in self:
            account_move = {
                "partner_id": record.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create({"name": percent_description, "quantity": 1, "price_unit": 0.06 * record.selling_price}),
                    Command.create({"name": admin_fee_description, "quantity": 1, "price_unit": 100.0}),
                ],
            }
            account_moves.append(account_move)

        # Note: account move creation does not work if fiscal localization is not set
        self.env["account.move"].create(account_moves)
        return result
