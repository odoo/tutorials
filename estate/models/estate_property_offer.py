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
        "Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline'
    )
    _offer_price_check = models.Constraint(
        'CHECK(price >= 0)', "Offer price should be strictly positive"
    )
    property_type_id = fields.Many2one(
        related='property_id.property_type_id', store=True)

    # DEPENDS DECORATOR
    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            start_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.date_deadline = start_date + \
                relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            start_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.validity = (record.date_deadline - start_date).days

    # BUTTON ACTION - OFFER
    def action_accept(self):
        if self.property_id.state == 'offer_accepted':
            raise UserError(
                "An offer has already been accepted for this property."
            )
        self.write({'status': 'accepted'})
        for offer in self:
            offer.property_id.write({
                'buyer_id': offer.partner_id.id,
                'selling_price': offer.price,
                'state': 'sold',
                'active': False
            })

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
            record.property_id.write({
                'buyer_id': None,
                'selling_price': None,
            })

    def create(self, vals):
        offer = super().create(vals)
        if offer.property_id and offer.property_id.state == 'new':
            offer.property_id.state = 'offer_received'

        return offer
