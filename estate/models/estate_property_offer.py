from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import date_utils


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = 'price desc'

    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one(
        'estate.property', string='Property', required=True, ondelete='cascade'
    )
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date(
        'Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline'
    )
    property_type_id = fields.Many2one(
        related='property_id.property_type_id', store=True
    )

    _check_price = models.Constraint(
        'CHECK(price > 0)', 'The price must be strictly positive.'
    )

    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = date_utils.add(
                (offer.create_date or fields.Date.today()), days=offer.validity
            )

    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (
                offer.date_deadline - (offer.create_date.date() or fields.Date.today())
            ).days

    @api.model
    def create(self, vals_list):
        for offer in vals_list:
            property_id = offer.get('property_id')
            if not property_id:
                continue

            linked_property = self.env['estate.property'].browse(property_id)

            lowest_price = min(linked_property.offer_ids.mapped('price'), default=0.0)
            if offer['price'] < lowest_price:
                raise UserError(
                    'You cannot create an offer with a lower amount than a existing one.'
                )

            if linked_property.state == 'new':
                linked_property.state = 'offer_received'
        return super().create(vals_list)

    def action_accept(self):
        for offer in self:
            other_offers = offer.property_id.offer_ids - offer
            if any(other_offers.filtered(lambda o: o.status == 'accepted')):
                raise UserError('An offer has already been accepted.')

            offer.status = 'accepted'
            offer.property_id.state = 'offer_accepted'
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
        return True

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
        return True
