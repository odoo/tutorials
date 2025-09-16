from datetime import date, timedelta
from odoo import api, exceptions, fields, models

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'
    _order = 'price desc'

    price = fields.Float("Price", required=True)
    _check_price = models.Constraint(
        'CHECK(price > 0)',
        "Price must be positive.",
    )

    status = fields.Selection(string="Status", selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @property
    def _create_date(self) -> date:
        if self.create_date:
            return self.create_date.date()
        else:
            return fields.Date.today()

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = offer._create_date + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - offer._create_date).days

    def action_accept(self):
        property_offer_to_accept_dict = dict() # maps each property to the offer we are going to accept for it
        for offer in self:
            if offer.property_id in property_offer_to_accept_dict:
                raise exceptions.UserError("Can't accept multiple offers for the same property")
            else:
                property_offer_to_accept_dict[offer.property_id] = offer

        for property_id, offer in property_offer_to_accept_dict.items():
            if property_id.buyer_id:
                raise exceptions.UserError("Property already has a buyer")
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
