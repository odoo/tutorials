from datetime import timedelta

from odoo import models, fields, api, exceptions


class EstatePropertyOffer(models.Model):

    _name = "estate.property.offer"
    _description = "Estate property offer"
    _order = "price desc"

    price = fields.Float("Offer Price")
    state = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one(string="Buyer", comodel_name="res.partner", required=True)
    property_id = fields.Many2one(comodel_name="estate.property", required=True)
    property_type_id = fields.Many2one(related="property_id.type_id", store=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date("Offer Deadline", compute="_compute_deadline", inverse="_inverse_deadline")

    _price_strictly_positive = models.Constraint(
        'CHECK(price > 0)',
        'Offer price must be strictly positive'
    )

    @api.depends("validity")
    def _compute_deadline(self):
        for offer in self:
            compare_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = compare_date + timedelta(days=offer.validity)

    def _inverse_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - offer.create_date.date()).days

    def action_accept_offer(self):
        for offer_to_accept in self:
            # Ensure there is no existing accepted offer
            if not offer_to_accept.property_id._no_accepted_offer():
                raise exceptions.UserError("Property already has an accepted offer.")

            offer_to_accept.state = "accepted"

            offer_to_accept.property_id.write({
                'buyer_id': offer_to_accept.partner_id.id,
                'state': 'offer_accepted',
                'selling_price': offer_to_accept.price,
            })

        return True

    def action_refuse_offer(self):
        for offer in self:
            # We could forbid refusing accepted offers
            offer.state = "refused"
        return True

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env['estate.property'].browse(vals['property_id'])
            if property.state == 'new':
                property.state = 'offer_received'
            elif property.state == 'sold':
                raise exceptions.UserError("Property already has been sold, new offers can not be created for it.")
        return super().create(vals_list)
