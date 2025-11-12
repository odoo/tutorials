from odoo import models, fields


class EstatePropertyOfferWizard(models.TransientModel):
    _name = "estate.property.offer.wizard"
    _description = "Wizard for Creating Offers on Properties"

    price = fields.Float(string="Offer Price", required=True)
    validity = fields.Integer(string="Validity (Days)", default=7, required=True)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Buyer", required=True)

    def action_make_offer(self):
        """Creates an offer for selected properties"""
        active_ids = self.env.context.get('active_ids',[])
        property_ids = self.env["estate.property"].browse(active_ids)
        vals_list = [{
            "price": self.price,
            "validity": self.validity,
            "partner_id": self.partner_id.id,
            "property_id": property.id
        } for property in property_ids]
        self.env["estate.property.offer"].create(vals_list)
