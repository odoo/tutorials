from odoo import models, fields, api
from odoo.exceptions import UserError

class EstateAddOfferWizard(models.TransientModel):
    _name = "estate.add.offer.wizard"
    _description = "Add Offer Wizard"

    property_id = fields.Many2many("estate.property", string="Properties")
    price = fields.Float(string="Offer Price", required=True)
    buyer_id = fields.Many2one("res.partner", string="Buyer", required=True)
    state = fields.Selection([
        ('new', 'New'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], string="Offer Status", default="new")

    def action_make_offer(self):
        if not self.property_id:
            raise UserError("Please select at least one property.")

        offer_model = self.env["estate.property.offer"]

        for property in self.property_id:
          
            if property.state in ['sold', 'cancelled']:
                continue

           
            offer_model.create({
                'property_id': property.id,
                'price': self.price,
                'partner_id': self.buyer_id.id,
                'state': self.state,
            })
            property.state = 'offer_received'

        return {'type': 'ir.actions.act_window_close'}



