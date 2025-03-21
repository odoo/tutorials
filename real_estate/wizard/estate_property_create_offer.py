from odoo import fields, models


class EstateCreateOffer(models.TransientModel):
    _name = "estate.create.offer"
    _description = "Make offer through wizard"

    price = fields.Float(string="Offered Price", required=True)
    partner_id = fields.Many2one("res.partner", string="Partner")

    def action_create_offer(self):
        active_ids = self.env.context.get("active_ids", [])  # Get selected property IDs
        if active_ids:
            offers = []
            for property_id in active_ids:
                print(self.partner_id.id)
                offers.append(
                    {
                        "price": self.price,
                        "partner_id": self.partner_id.id,
                        "property_id": property_id,
                    }
                )
            self.env["estate.property.offer"].create(offers)
