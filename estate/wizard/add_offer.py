from odoo import fields, models


class AddOffer(models.TransientModel):
    _name = "estate.add.offer"
    _description = "Add Offer to Selected Properties"

    property_ids = fields.Many2many("estate.property", string="Properties")
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    price = fields.Float(string="Offer Price", default=500000, required=True)

    def action_add_offer(self):
        all_properties = self.property_ids.env["estate.property"].search([["property_type_id.name", "=", "flat"]])

        vals_list = []
        for record in all_properties:
            vals_dict = {
                "property_id": record.id,
                "price": self.price,
                "partner_id": self.partner_id.id,
            }
            vals_list.append(vals_dict)

        self.env["estate.property.offer"].create(vals_list)
        return True
