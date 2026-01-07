from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', "Accepted"), ('refused', "Refused")], copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        "Deadline", compute='_compute_validity', inverse='_inverse_validity'
    )
    _offer_price_check = models.Constraint(
        'CHECK(price >= 0)', "Offer price should be strictly positive"
    )

    # DEPENDS DECORATOR
    @api.depends('validity', 'create_date')
    def _compute_validity(self):
        for record in self:
            start_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.date_deadline = start_date + relativedelta(days=record.validity)

    def _inverse_validity(self):
        for record in self:
            start_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.validity = (record.date_deadline - start_date).days

    # BUTTON ACTION - OFFER
    def action_accept(self):
        for record in self:
            if record.property_id.state != 'offer_accepted' and record.property_id.state not in ('cancelled', 'sold'):
                record.status = 'accepted'
                record.property_id.buyer_id = self.partner_id
                record.property_id.selling_price = record.price
                record.property_id.state = 'offer_accepted'
            else:
                raise UserError(f"One offer has already been ({record.property_id.state})")

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
            record.property_id.state = 'new'
            record.property_id.buyer_id = None
            record.property_id.selling_price = None
