# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, exceptions, fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Real Estate Property Offer"
    _explanation = "Defines an offer on real estate property"
    _order = "price desc"

    price = fields.Float('Price', required=True)
    status = fields.Selection(
        string='Status',
        selection=[('offer_accepted', 'Accepted'), ('offer_refused', 'Refused')],
        copy=False,
        help="Status of the offer")
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date('Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one('estate.property.type', related='property_id.property_type_id',
                                       string='Property type', store=True)

    _check_prices = models.Constraint(
        'CHECK(price > 0.0)',
        'The expected and selling price must be strictly positive.',
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = fields.Date.add(offer.create_date or fields.Date.today(), days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - fields.Date.to_date(offer.create_date)).days

    @api.model
    def create(self, vals_list):
        property = self.env['estate.property'].browse(vals_list[0]['property_id'])
        for record_vals in vals_list:
            if property.state == 'sold':
                raise exceptions.UserError(
                    self.env._("%(property)s: It is not allowed to add an offer for a sold property",
                               property=property.name))
            partner = self.env['res.partner'].browse(record_vals['partner_id'])
            if record_vals['price'] <= property.best_price:
                raise exceptions.UserError(
                    self.env._("%(buyer)s's offer at %(offer_price).2f may not be lower than %(best_price).2f",
                               buyer=partner.name,
                               offer_price=record_vals['price'],
                               best_price=property.best_price))
            property.state = 'offer_received'
        return super().create(vals_list)

    def action_accept_property_offer(self):
        offer = self.ensure_one()
        property = offer.property_id
        if property.state in ('new', 'offer_received'):
            offer.status = 'offer_accepted'
            property.selling_price = offer.price
            property.buyer_id = offer.partner_id
            property.state = 'offer_accepted'
        else:
            raise exceptions.UserError(self.env._("Another offer has already been accepted!"))
        return True

    def action_refuse_property_offer(self):
        for record in self:
            if record.status == 'offer_accepted':
                raise exceptions.UserError(self.env._("Once accepted, an offer cannot be refused!"))
            record.status = 'offer_refused'
        return True
