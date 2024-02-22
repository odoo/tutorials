from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    _sql_constraints = [('check_price', 'CHECK(price > 0)', 'The offer price must be strictly positive.')]

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = fields.Date.add(date, days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days

    def action_property_offer_accepted(self):
        for offer in self:
            if offer.property_id.selling_price:
                raise UserError("Can't accept more than one offer for a property!")
            offer.status = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer = offer.partner_id
        return True

    def action_property_offer_refused(self):
        for offer in self:
            if offer.status == 'accepted':
                raise UserError("Can't refuse an already accepted offer!")
            offer.status = 'refused'
        return True

    @api.model
    def create(self, vals):
        estate_property = self.env['estate.property'].browse(vals['property_id'])
        if vals['price'] < estate_property.best_price:
            raise UserError("Can't create an offer with a price less than the best offer!")
        estate_property.state = 'offer_received'
        return super().create(vals)
