from odoo import fields, models


class EstatePropertyWizard(models.TransientModel):
    _name = "estate.property.wizard"
    _description = "Create Offers"

    price = fields.Float()

    partner_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False,
    )

    def action_create_offers(self):

        properties = self.env["estate.property"].search([
            ("state", "not in", ["sold", "canceled", "offer_accepted"])
        ])
        for property in properties:
            self.env["estate.property.offer"].create({
                "price": self.price,
                "partner_id": self.partner_id.id,
                "property_id": property.id,
                    })
        return True
