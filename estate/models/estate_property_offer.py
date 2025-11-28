from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offers"
    _order = "price desc"

    price = fields.Float("Price", required=True)
    state = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        string="Status",
        default=False,
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        store=True,
        string="Property Type",
    )
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date(
        "Deadline", compute="_compute_date_deadline", store=True
    )

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                base_dt = fields.Datetime.from_string(offer.create_date)
            else:
                base_dt = fields.Datetime.now()
            deadline_dt = base_dt + timedelta(days=offer.validity or 0)
            offer.date_deadline = fields.Date.to_string(deadline_dt.date())

    def action_accept(self):
        for offer in self:
            offer.state = 'accepted'
            offer.property_id.write(
                {
                    'selling_price': offer.price,
                    'buyer_id': offer.partner_id.id,
                    'state': 'offer_accepted',
                }
            )
            other_offers = offer.property_id.offer_ids.filtered(
                lambda o: o.id != offer.id and o.state != 'refused'
            )
            other_offers.state = 'refused'
        return True

    def action_refuse(self):
        for offer in self:
            offer.state = 'refused'
        return True

    @api.model
    def create(self, vals_list):
        if isinstance(vals_list, dict):
            vals_list = [vals_list]

        for vals in vals_list:
            prop_id = vals.get('property_id')
            price = vals.get('price')
            if prop_id and price is not None:
                prop = self.env['estate.property'].browse(prop_id)
                existing_prices = prop.offer_ids.mapped('price')
                if existing_prices:
                    best = max(existing_prices)
                    if float_compare(price, best, precision_digits=2) < 0:
                        raise ValidationError(
                            'You cannot create an offer lower than an existing offer.'
                        )

        offers = super().create(vals_list)

        for offer in offers:
            if offer.property_id:
                offer.property_id.state = 'received'
        return offers
