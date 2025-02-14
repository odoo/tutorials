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

        for record in self:
            self.env["account.move"].create(
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

        return super().action_set_property_status_sold()
