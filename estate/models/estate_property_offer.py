from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', "Accepted"), ('refused', "Refused")], copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        "Deadline", compute='_compute_deadline', inverse='_inverse_deadline'
    )
    _offer_price_check = models.Constraint(
        'CHECK(price >= 0)', "Offer price should be strictly positive"
    )
    property_type_id = fields.Many2one(
        related='property_id.property_type_id', store=True)
    check_button = fields.Char(store=False)

    # DEPENDS DECORATOR
    @api.depends('validity', 'create_date')
    def _compute_deadline(self):
        for record in self:
            start_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.date_deadline = start_date + \
                relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            start_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.validity = (record.date_deadline - start_date).days

    @api.depends("property_id.offers_id")
    def _compute_offer(self):
        #     for record in self:
        #         if record.property_id.buyer_id and record.property_id.buyer_id != record.partner_id:
        #             record.check_button = True
        #         else:
        #             record.check_button = False

        for record in self.property_id.offers_id:
            record.check_button = self.property_id.offers_id.filtered_domain([
                ('status', 'in', ('accepted', 'refused'))
            ])

    # BUTTON ACTION - OFFER
    def action_accept(self):
        for offer in self:
            if offer.property_id.buyer_id:
                raise UserError(
                    "An offer has already been accepted for this property.")

            offer.status = 'accepted'
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.property_id.state = 'offer_accepted'

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
            record.property_id.buyer_id = None
            record.property_id.selling_price = None
            record.property_id.state = 'offer_received'

    # OFFER ADDED - STATE CHANGE TO OFFER_RECEIVED
    def create(self, vals):
        offer = super().create(vals)
        if offer.property_id and offer.property_id.state == 'new':
            offer.property_id.state = 'offer_received'

        return offer
