from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        selection = [
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        copy = False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7, help='Validity in days')
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline", readonly=False)

    @api.depends('validity')
    def _compute_deadline(self):
        for ofr in self:
            if isinstance(ofr.create_date,bool):
               ofr.date_deadline = fields.Date.today() + relativedelta(days=ofr.validity)
            else:
               ofr.date_deadline = ofr.create_date + relativedelta(days=ofr.validity)


    def _inverse_deadline(self):
        for ofr in self:
            ofr.validity = (ofr.date_deadline - ofr.create_date.date()).days 


    def accept_offer(self):
        for offer in self:
            other_accepted = offer.property_id.offer_ids.filtered(lambda o: o.status == 'accepted' and o != offer)
            if other_accepted:
                raise UserError("Only one offer can be accepted.")
            
            offer.status = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer = offer.partner_id
        return True

    

    def refuse_offer(self):
        self.status = 'refused'
        return True

