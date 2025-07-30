from odoo import api, fields, models

class estateOfferWizard(models.TransientModel):
    _name = "estate.offer"
    _description = "add offer to multiple properties"   

    price = fields.Integer(string = "price")
    validity = fields.Integer(string="Validity (Days)", default=7)
    buyer_id = fields.Many2one("res.partner", string = "Buyer", required = True)

    def make_offer(self):
        """Add an offer to each selected property"""
        properties = self.env["estate.property"].browse(self.env.context.get('active_ids', []))
        for property in properties:
            self.env["estate.property.offer"].create({
                "property_id": property.id,
                "price": self.price,
                "validity": self.validity,
                "partner_id":self.buyer_id.id,
            })
