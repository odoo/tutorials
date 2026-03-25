from odoo import _, fields, models


class EstatePropertyWizard(models.TransientModel):
    _name = "estate.property.wizard"
    _description = "Find Property Offers"

    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type", required=True,
    )
    expected_price = fields.Float(string="Maximum Price", required=True)
    buyer_id = fields.Many2one("res.partner", string="Buyer", required=True)

    def action_find_offers(self):

        self.ensure_one()
        properties = self.env["estate.property"].search([
            ("property_type_id", "=", self.property_type_id.id),
            ("expected_price", "<=", self.expected_price),
            ("best_price", "<", self.expected_price),
            ("state", "in", ("new", "offer_received")),
        ])

        offers = self.env["estate.property.offer"].create([
                {
                    "property_id": prop.id,
                    "partner_id": self.buyer_id.id,
                    "price": self.expected_price,
                }
                for prop in properties
        ])
        return {
            "name": _("Created Offers"),
            "type": "ir.actions.act_window",
            "res_model": "estate.property.offer",
            "view_mode": "list",
            "domain": [("id", "in", offers.ids)],
            "target": "current",
        }
