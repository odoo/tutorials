from odoo import fields, models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def _create_account_move(self):
        for offer in self.offer_ids:
            if offer.status == 'accepted':
                move = self.env['account.move'].create([
                    dict(
                        partner_id=offer.partner_id.id,
                        move_type="out_invoice",
                        line_ids=[
                            Command.create(dict(name="6% Down Payment", quantity=0.06, price_unit=offer.price)),
                            Command.create(dict(name="Administrative Fees", quantity=1, price_unit=100))
                        ]
                    )]
                )

    def action_property_sold(self):
        for property in self:
            property._create_account_move()

        return super().action_property_sold()
