from odoo import models, fields,api


class MakeOfferWizard(models.TransientModel):
    _name = "make.offers.wizard"
    _description = "Make Offers Wizard"

    price = fields.Float()
    partner_id = fields.Many2one("res.partner", "Buyer", required=True)
    validity = fields.Integer(default=7)

    def make_offer(self):
        property_ids = self._context.get('active_ids',[])

        offer = {
            'price':self.price,
            'validity':self.validity,
            'partner_id':self.partner_id.id
        }

        for property in self.env['estate.property'].browse(property_ids):
            self.env['estate.property.offer'].create({**offer,'property_id':property.id})
