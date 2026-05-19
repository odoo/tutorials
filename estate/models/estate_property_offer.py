from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import _, api, exceptions, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer Model"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ], copy=False
    )
    validity = fields.Integer(default=7)

    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(
        related='property_id.property_type_id',
    )
    date_deadline = fields.Date(
        compute='_compute_deadline_date',
        inverse='_inverse_deadline_date',
    )

    _check_offer_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be stricly positive.'
    )

    @api.depends('validity')
    def _compute_deadline_date(self):
        for record in self:
            record.date_deadline = (record.create_date or date.today()) + relativedelta(
                days=record.validity
            )

    def _inverse_deadline_date(self):
        for record in self:
            start_date = (
                record.create_date.date() if record.create_date else date.today()
            )

            record.validity = (record.date_deadline - start_date).days

    def action_accept(self):
        for record in self:
            if any(
                offer.status == "accepted" and record.id != offer.id
                for offer in record.property_id.offer_ids
            ):
                raise exceptions.UserError(
                    'A property can only have one accpeted Offer')
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'offer_accepted'

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
            record.property_id.selling_price = None
            record.property_id.buyer_id = None

    @api.model
    def create(self, vals_list):
        property_id = None
        price = 0
        for vals in vals_list:
            val_property_id = vals.get('property_id')
            val_price = vals.get('price')
            if val_property_id:
                property_id = val_property_id
            if val_price is not None:
                price = val_price

        property_record = self.env['estate.property'].browse(property_id)
        if any(
            offer.price > price
            for offer in property_record.offer_ids
        ):
            raise exceptions.UserError(
                _('Can\'t create an offer with a lower price than an existing offer.')
            )
        property_record.state = 'offer_received'
        return super().create(vals_list)
