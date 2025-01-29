from odoo import api, fields, models
from odoo.exceptions import UserError

class Offer(models.Model):
    _name = 'estate.house.offer'
    _description = 'House Offer Model'
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', "offer price can't be negative")
    ]
    _order = 'price desc'

    price = fields.Float(required=True)
    status = fields.Selection(selection=[
        ('accepted','Accepted'),
        ('refused','Refused')
    ], copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.house', 'Property applied on', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_offer_deadline", inverse="_inverse_offer_deadline")
    property_type = fields.Many2one(related='property_id.house_type_id')

    @api.model
    def create(self, vals):
        house = self.env["estate.house"].browse(vals["property_id"])
        smaller_offers = self.env["estate.house.offer"].search_count([('price', '>', vals['price'])], limit=1)
        if(smaller_offers > 0):
            raise UserError("Can't create offer with price less than one of the existing offers")
        house.state = 'offer_received'
        return super().create(vals)

    @api.depends("validity")
    def _compute_offer_deadline(self):
        for offer in self:
            current_date = offer.create_date or fields.Date.today()
            offer.date_deadline = fields.Date.add(current_date, days=offer.validity)

    def _inverse_offer_deadline(self):
        for offer in self:
            current_date = fields.Date.to_date(offer.create_date or fields.Date.today())
            offer.validity = (offer.date_deadline - current_date).days

    def accept_offer(self):
        for offer in self:
            property = offer.property_id
            if(property.state == 'offer_accepted'):
                raise UserError('This property has already accepted an offer')
            offer.status = 'accepted'
            property.state = 'offer_accepted'
            property.selling_price = offer.price
            property.buyer_id = offer.partner_id
    
    def reject_offer(self):
        for offer in self:
            offer.status = 'refused'
