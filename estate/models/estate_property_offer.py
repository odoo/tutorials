from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate Property Offer"
    _order = 'price desc'
    
    price = fields.Float(required=True)
    property_id = fields.Many2one('estate.property', required=True)
    partner_id = fields.Many2one('res.partner', required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)
    status = fields.Selection([
        ('accepted', "Accepted"),
        ('refused', "Refused")
    ], copy=False)
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days
    
    def action_accept_offer(self):
        self.ensure_one()
        for offer in self:
            if any(offer.property_id.offer_ids.mapped('status')):
                raise UserError("An offer has already been accepted or refused for this property.")
            offer.status = 'accepted'
            offer.property_id.state = 'offer_accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
        return True

    def action_reject_offer(self):
        for offer in self:
            offer.status = 'refused'
        return True

    _check_offer_price = models.Constraint(
        'CHECK(price > 0)',
        "The offer price should be strictly positive"
    )
