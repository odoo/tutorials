from odoo import models, fields, api

class EstatePropertyOfferWizard(models.TransientModel):
    _name = "estate.property.offer.wizard"
    _description = "Wizard for adding offers to multiple properties"

    property_ids = fields.Many2many("estate.property", string="properties", required=True)
    price = fields.Float(string="Offer Price", required=True)
    validity = fields.Integer(string="Validity (days)", default=7, required=True)
    buyer_id = fields.Many2one("res.partner", string="Buyer", required=True)

    def action_create_offer(self):
        for property in self.property_ids:
            self.env["estate.property.offer"].create({
                "property_id": property.id,
                "price": self.price,
                "validity": self.validity,
                "partner_id": self.buyer_id.id,
            })

        return {"type": "ir.actions.act_window_close"}
