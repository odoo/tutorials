from datetime import date, timedelta
from typing import TYPE_CHECKING
from odoo import api, fields, models
from odoo.exceptions import UserError

if TYPE_CHECKING:
    from estate.models.estate_property import EstateProperty

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Property Offer"
    _order = 'price desc'

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        "Price must be positive.",
    )

    price = fields.Float("Price", required=True)
    status = fields.Selection(string="Status", selection=[('accepted', "Accepted"), ('refused', "Refused")], copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id', string="Property Type", stored=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = offer._create_date + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - offer._create_date).days

    @api.model
    def create(self, vals_list):
        property: "EstateProperty" = self.env['estate.property'].browse(vals_list[0]['property_id'])
        if vals_list[0]['price'] < property.best_price:
            raise UserError("Can't create an Offer with price lower than the Property's best price")
        property.state = 'offer_received'
        return super().create(vals_list)

    def action_accept(self):
        property_offer_to_accept_dict = dict() # maps each property to the offer we are going to accept for it
        for offer in self:
            if offer.property_id in property_offer_to_accept_dict:
                raise UserError("Can't accept multiple offers for the same property")
            else:
                property_offer_to_accept_dict[offer.property_id] = offer

        for property_id, offer in property_offer_to_accept_dict.items():
            if property_id.buyer_id:
                raise UserError("Property already has a buyer")
            else:
                offer.status = 'accepted'
                property_id.buyer_id = offer.partner_id
                property_id.selling_price = offer.price
                property_id.state = 'offer_accepted'
                for other_offer in property_id.offer_ids:
                    if other_offer.id != offer.id:
                        other_offer.status = 'refused'
        return True

    def action_refuse(self):
        for offer in self:
            if offer.status == 'accepted':
                # if it was previously accepted, we want to undo setting the fields on the property:
                offer.property_id.buyer_id = None
                offer.property_id.selling_price = None
            offer.status = 'refused'
        return True

    @property
    def _create_date(self) -> date:
        if self.create_date:
            return self.create_date.date()
        else:
            return fields.Date.today()
