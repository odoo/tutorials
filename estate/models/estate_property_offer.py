from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float('Price', required=True)
    property_id = fields.Many2one('estate.property', 'property_id', required=True)
    partner_id = fields.Many2one('res.partner', required=True)
    status = fields.Selection(
        string='Status',
        copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
    )
    property_type_id = fields.Many2one(related="property_id.type_id", store=True)
    validity = fields.Integer(
        "Validity (days)",
        default=7,
        required=True,
    )
    date_deadline = fields.Date(
        "Deadline",
        required=True,
        compute="_compute_deadline",
        inverse="_inverse_deadline",
    )

    @api.depends("validity")
    def _compute_deadline(self):
        for offer in self:
            offer.date_deadline = fields.Date.today() + relativedelta(days=offer.validity)

    def _inverse_deadline(self):
        for offer in self:
            delta = offer.date_deadline - fields.Date.today()
            offer.validity = delta.days

    def action_offer_accept(self):
        for offer in self:
            if offer.property_id.state in ('offer_accepted', 'sold', 'cancelled'):
                raise UserError("You can not accept more offers for this property")

            offer.status = "accepted"
            offer.property_id.state = "offer_accepted"
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price

        return True

    def action_offer_refuse(self):
        for offer in self:
            offer.status = "refused"

        return True

    _price_positive = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be strictly positive',
    )

    @api.model_create_multi
    def create(self, values):
        # Get the lowest new offer per property
        prop_min_offer = {}
        for v in values:
            pid = v['property_id']
            prop_min_offer[pid] = min(prop_min_offer.get(pid, float('inf')), v.get('price', 0))

        # Browse the properties referenced by the new offers
        properties = self.env['estate.property'].browse(prop_min_offer.keys())

        for prop in properties:
            # No new offer may be lower than the best existing one
            best_existing = prop.offer_ids[0]
            if prop_min_offer[prop.id] < best_existing:
                raise UserError("You can not offer less than the biggest offer")

        properties.filtered(lambda p: p.state == 'new').state = 'offer_received'

        return super().create(values)
