from odoo import fields, models


class EstateListWizard(models.TransientModel):
    _name = "estate.wizard"
    _description = "A Simple Wizard"

    price = fields.Float(string="Price")
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)

    def action_give_offer(self):
        properties = self.env["estate.property"].browse(self.env.context.get("active_ids"))
        vals_list = []
        for prop in properties:
            vals_list.append(
                {
                    "property_id": prop.id,
                    "price": self.price,
                    "partner_id": self.partner_id.id,
                }
            )

        self.env["estate.property.offer"].create(vals_list)
