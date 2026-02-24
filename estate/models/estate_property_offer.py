from datetime import timedelta

from odoo import api, models, fields
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="Offer Price")
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        required=True,
    )
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True,
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        store=True
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    _price_check = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be strictly positive.'
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - create_date).days

    @api.model_create_multi
    def create(self, vals_list):
        offers = super().create(vals_list)
        for offer in offers:
            property_rec = offer.property_id
            if property_rec.state in ['offer_accepted', 'sold', 'cancelled']:
                raise UserError("Cannot create offer for this property.")
            if property_rec.state == 'new':
                property_rec.state = 'offer_received'
        return offers

    def action_accept(self):
        for offer in self:
            property = offer.property_id
            minimum_price = property.expected_price * 0.9
            if float_compare(offer.price, minimum_price, precision_digits=2) < 0:
                raise ValidationError(
                    "The selling price must be at least 90% of the expected price! "
                    "You must reduce the expected price if you want to accept this offer."
                )
            if offer.property_id.state in ['sold', 'cancelled']:
                raise UserError("You cannot accept an offer on a sold or cancelled property.")
            accepted_offer = offer.property_id.offer_ids.filtered(
                lambda o: o.status == "accepted" and o != offer
            )
            if accepted_offer:
                raise UserError("Only one offer can be accepted for a property.")
            offer.status = "accepted"
            offer.property_id.write({
                'selling_price': offer.price,
                'buyer_id': offer.partner_id.id,
                'state': 'offer_accepted'
            })
            
            other_pending_offers = offer.property_id.offer_ids.filtered(
                lambda o: o.status != 'refused' and o != offer
            )
            other_pending_offers.write({'status': 'refused'})

    def action_refuse(self):
        for offer in self:
            property_rec = offer.property_id
            if property_rec.state in ['sold', 'cancelled']:
                raise UserError("You cannot refuse an offer on a sold or cancelled property.")
            if offer.status == "accepted":
                offer.status = "refused"
                property_rec.write({
                    'selling_price': 0.0,
                    'buyer_id': False,
                })
                other_pending = property_rec.offer_ids.filtered(
                    lambda offer: offer.status == 'refused'
                )
                if other_pending:
                    property_rec.state = 'offer_received'
                else:
                    property_rec.state = 'new'
            else:
                offer.status = "refused"
