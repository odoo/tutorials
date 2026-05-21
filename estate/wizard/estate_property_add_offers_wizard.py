from odoo import models, fields, Command


class EstatePropertyAddOffersWizard(models.TransientModel):
    _name = "estate.property.add.offers.wizard"
    _description = "description"

    starting_range = fields.Float(required=True)
    ending_range = fields.Float(required=True)
    offer_price = fields.Float(required=True)
    property_type_id = fields.Many2one("estate.property.type")

    def add_offers(self):
        for record in self:
            if record.property_type_id:
                properties = self.env["estate.property"].search(
                    [
                        ("expected_price", ">", record.starting_range),
                        ("expected_price", "<", record.ending_range),
                        ("property_type_id", "=", record.property_type_id),
                    ]
                )
            else:
                properties = self.env["estate.property"].search(
                    [
                        ("expected_price", ">", record.starting_range),
                        ("expected_price", "<", record.ending_range),
                    ]
                )

            filtered_properties = properties.filtered(
                lambda property: property.best_price < record.offer_price
            )
            filtered_properties.write(
                {
                    "offer_ids": [
                        Command.create(
                            {
                                "price": record.offer_price,
                                "partner_id": record.env.user.partner_id.id,
                            }
                        )
                    ]
                }
            )
            return {
                "effect": {
                    "fadeout": "slow",
                    "message": f"{len(filtered_properties)} offers are created.",
                    "img_url": "/web/static/img/smile.svg",
                    "type": "rainbow_man",
                }
            }
