from odoo import fields, models


class AddOffer(models.TransientModel):
    _name = "property.offer.wizard"
    _description = "Add offer"
    _order = "price desc"

    price = fields.Float(string="Price", required=True)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    create_date = fields.Datetime(string="Creation Date", default=fields.Datetime.now)

    def action_make_offer(self):
        context = self.env.context
        print(context)
        active_ids = context.get("active_ids", [])
        for property_id in active_ids:
            self.env["estate.property.offer"].create(
                {
                    "price": self.price,
                    "validity": self.validity,
                    "partner_id": self.partner_id.id,
                    "property_id": property_id,
                }
            )
