from odoo import models, fields, api

class EstateAddOfferWizard(models.TransientModel):
    _name = "estate.add.offer.wizard"
    _description = "Add Offer Wizard"

    price = fields.Float(string="Offer Price", required=True)
    buyer_id = fields.Many2one(comodel_name="res.partner", string="Buyer", required=True)

    def make_offer(self):
        active_ids = self._context.get('active_ids', [])
        properties = self.env['estate.property'].browse(active_ids)
        active_properties = []
        for property in properties:
            if property.state in ["new", "offer_received"]:
                active_properties.append(property)
        for property in active_properties:
            self.env["estate.property.offer"].create({
                "price": self.price,
                "property_id": property.id,
                "partner_id": self.buyer_id.id
            })
            property.state = "offer_received"
        return {"type": "ir.actions.act_window_close"}
