from odoo import Command, models


class EstateAccountProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        for property_record in self:
            self.env['account.move'].create(
                [
                    dict(
                        partner_id=property_record.buyer_id.id,
                        move_type="out_invoice",
                        line_ids=[
                            Command.create(dict(name="6% Down Payment", quantity=1,
                                                price_unit=0.06 * property_record.selling_price)),
                            Command.create(dict(name="Administrative Fees", quantity=1, price_unit=100))
                        ],

                    )
                ]
            )
        return super().action_sold()
