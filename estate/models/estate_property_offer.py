from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order="price desc"

    price = fields.Float(string='Price')
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')],string='Status',copy=False)
    partner_id = fields.Many2one('res.partner',string='Buyer',required=True)
    property_id = fields.Many2one('estate.property',string='Property',required=True,ondelete='cascade')
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Date Deadline',compute='_compute_date_deadline',inverse='_inverse_date_deadline',store=True)
    property_type_id = fields.Many2one(
    "estate.property.type",
    string="Property Type",
    related="property_id.property_type_id",
    store=True
)

    _sql_constraints = [
        ('check_offer_price_positive', 'CHECK(price > 0)', 'The offer price must be strictly positive.'),
    ]
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.context_today(record)
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Datetime.now()
            delta = record.date_deadline - create_date.date()
            record.validity = delta.days

    def action_accept(self):
        for offer in self:
            if offer.property_id.state in ['sold', 'cancelled']:
                raise UserError("You cannot accept an offer for a sold or cancelled property.")
            if offer.property_id.offer_ids.filtered(lambda o: o.status == 'accepted'):
                raise UserError("An offer has already been accepted for this property.")
            offer.status = 'accepted'
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.property_id.state = 'offer_accepted'
            # self.env.refresh_all() 
            return True

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
            # self.env.refresh_all()  # <-- Add this line
            return True  # Optional but helps refresh