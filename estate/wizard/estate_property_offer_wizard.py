from datetime import timedelta

from odoo import fields, models
from odoo.exceptions import UserError

class EstatePropertyOfferWizard(models.TransientModel):
    _name = "estate.property.offer.wizard"
    _description = "Estate Property Offer Wizard"

    price = fields.Float(string="Price", required=True)
    buyer_id = fields.Many2one("res.partner", string="Partner", required=True)
    date_deadline = fields.Date("Deadline", default=lambda self: fields.Date.today() + timedelta(days=7), required=True)

    

    def add_offers_to_multiple_properties(self):
        selected_properties = self.env['estate.property'].browse(self.env.context.get('active_ids', []))

        offer_price = self.price
        offer_buyer_id = self.buyer_id
        offer_date_deadline = self.date_deadline

        for property in selected_properties:

            if property.state == 'sold':
                raise UserError(f"The property '{property.name}' is alredy sold ")

            self.env['estate.property.offer'].create({
                'price' : offer_price,
                'partner_id' : offer_buyer_id.id,
                'date_deadline':offer_date_deadline,
                'property_id' : property.id
            })
        return {'type': 'ir.actions.act_window_close'}
