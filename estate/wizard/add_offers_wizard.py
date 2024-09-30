from odoo import fields, models


class addofferproperties(models.TransientModel):
    _name = "add.offers.wizard"
    _description = "wizard for adding offers to properties"

    price = fields.Float(required=True)
    status = fields.Selection(
        [("Accepted", "Accepted"), ("Refused", "Refused")], string="Status", copy=False
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", required=True)

    def add_offer_properties(self):
        active_ids = self.env.context.get("active_ids", [])
        properties = self.env["estate.property"].browse(active_ids)
        for ele in properties:
            self.env["estate.property.offer"].create(
                {
                    "property_id": ele.id,
                    "price": self.price,
                    "status": self.status,
                    "partner_id": self.buyer_id.id,
                }
            )
