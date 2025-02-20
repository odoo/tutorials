from odoo import  Command, models
class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_property_status_sold(self):

        # access is already checked in .create() method, checking it again add redundancy

        # if not self.env["account.move"].check_access_rights("create", False):
        #     try:
        #         self.check_access_rights("write")
        #         self.check_access_rule("write")
        #     except AccessError:
        #         return self.env["account.move"]
        print(" reached ".center(100, '='))

        is_sold = super().action_set_property_status_sold()

        print(self.env.user)
        print(self.env.user.has_group)
        self.env["account.move"].check_access("write")
        if (is_sold):
            for record in self:
                # sudo to bypass access and record rules to any user
                self.env["account.move"].sudo().create(
                    {
                        "partner_id": record.buyer_id.id,
                        "move_type": "out_invoice",
                        "invoice_line_ids": [
                            Command.create(
                                {
                                    "name": "6% of Selling Price",
                                    "quantity": 1,
                                    "price_unit": 0.6 * record.selling_price,
                                }
                            ),
                            Command.create(
                                {
                                    "name": "Administration Fee",
                                    "quantity": 1,
                                    "price_unit": 100,
                                }
                            ),
                        ],
                    }
                )

        return is_sold
