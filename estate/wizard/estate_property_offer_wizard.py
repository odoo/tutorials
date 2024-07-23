from odoo import fields, models
from dateutil.relativedelta import relativedelta


class EstatePropertyOfferWizard(models.TransientModel):
    _name = "estate.property.offer.wizard"
    _description = "Wizard to Add Offer to Properties"

    price = fields.Float(string="Offer Price")
    partner_id = fields.Many2one("res.partner", string="Buyer")
    date_deadline = fields.Date("Deadline", default=fields.Datetime.today() + relativedelta(days=7))

    def make_offer(self):
        active_ids = self.env.context.get("active_ids")
        for prop in active_ids:
            self.env["estate.property.offer"].create(
                {
                    "property_id": prop,
                    "price": self.price,
                    "date_deadline": self.date_deadline,
                    "partner_id": self.partner_id.id,
                }
            )
        return {"type": "ir.actions.act_window_close"}
