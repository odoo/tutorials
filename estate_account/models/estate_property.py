from odoo import Command, models

# Commission invoiced to the buyer, as a ratio of the selling price.
COMMISSION_RATE = 0.06
# Fixed administrative fees invoiced for each sold property.
ADMINISTRATIVE_FEES = 100.0


class EstateProperty(models.Model):
    """Invoice the buyer when a property is sold."""

    _name = "estate.property"
    _inherit = ["estate.property"]

    def action_sold(self):
        """Sell the properties, then create one customer invoice per property.

        The sale checks are done by super(): if a property cannot be sold, an
        error is raised before any invoice is created.
        """
        res = super().action_sold()
        self.env["account.move"].create(
            [record._prepare_invoice_values() for record in self]
        )
        return res

    def _prepare_invoice_values(self):
        """Return the values of the customer invoice of the property.

        Kept in a dedicated method so that other modules can extend the
        invoice without overriding the whole sale.
        """
        self.ensure_one()
        return {
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "invoice_line_ids": [
                Command.create({
                    "name": self.name,
                    "quantity": 1,
                    "price_unit": self.selling_price * COMMISSION_RATE,
                }),
                Command.create({
                    "name": self.env._("Administrative fees"),
                    "quantity": 1,
                    "price_unit": ADMINISTRATIVE_FEES,
                }),
            ],
        }
