from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class NinjaTurtlesEstatePropertyOffer(models.Model):
    _name = "ninja.turtles.estate.property.offer"
    _description = "Ninja Turtles Estate for faster Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price")
    offer_status = fields.Selection(
        string="Offer Status",
        selection=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        default='pending',
        copy=False,
    )
    validity = fields.Integer(
        string="Validity (days)",
        default=7,
    )
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        required=True,
    )
    property_id = fields.Many2one(
        "ninja.turtles.estate",
        string="Property",
        required=True,
        ondelete="cascade",                 # its kinda weird cuz it should only be on the property model
    )
    property_type_id = fields.Many2one(
    "ninja.turtles.estate.property.type",
        related='property_id.property_type_id',
        store=True,
    )

    _sql_constraints = [
        ('check_offer_price_positive', 'CHECK(price > 0)', 'Offer price must be strictly positive.'),
    ]

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            # Fallback for create_date, use today's date if missing (e.g. during creation)
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            # Fallback for create_date if missing
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            if record.date_deadline:
                delta = record.date_deadline - create_date
                record.validity = delta.days
            else:
                record.validity = 0

    @api.model_create_multi
    def create(self, vals_list):
        offer_cnt = 1

        for vals in vals_list:
            property_id = vals.get('property_id')
            if property_id:
                property = self.env['ninja.turtles.estate'].browse(property_id)

                max_offer = max(property.offer_ids.mapped('price'), default=0)
                if vals['price'] < max_offer:
                    raise UserError(f"You cannot create an offer lower than an existing offer.\n"
                                    f"New offer in line_{offer_cnt} is causing an issue for now.")
                property.status = 'offer received'
            offer_cnt = offer_cnt + 1

        return super().create(vals_list)

    def action_accept(self):
        for offer in self:
            if offer.property_id.status in ['sold', 'cancelled']:
                raise UserError("You cannot accept an offer for a sold or cancelled property.")

            other_offers = offer.property_id.offer_ids - offer
            other_offers.write({'offer_status': 'refused'})

            offer.offer_status = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.status = 'offer accepted'
        return True

    def action_refuse(self):
        for offer in self:
            if offer.offer_status != 'accepted':
                offer.offer_status = 'refused'
        return True
