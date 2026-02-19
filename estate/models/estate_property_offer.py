from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float(required=True)
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        string="Status",
        copy=False
    )
    partner_id = fields.Many2one(
        'res.partner',
        string="Buyer",
        required=True
    )
    property_id = fields.Many2one(
        'estate.property',
        string="Property",
        required=True,
        ondelete='restrict'
    )

    property_type_id = fields.Many2one(
        'estate.property.type',
        string="Property Type",
        related='property_id.property_type_id',
        store=True
    )

    validity = fields.Integer(
        string="Validity (days)",
        default=7
    )

    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )
    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - create_date).days

    def action_accept(self):
        for offer in self:
            property = offer.property_id
            # Check if another offer was already accepted
            if property.offer_ids.filtered(lambda o: o.status == 'accepted'):
                raise UserError("Only one offer can be accepted per property.")
            # Refuse others offers
            other_offers = property.offer_ids.filtered(lambda o: o != offer)
            other_offers.write({'status': 'refused'})
            # Accept current offer
            offer.status = 'accepted'
            property.selling_price = offer.price
            property.buyer_id = offer.partner_id
            property.state = 'offer_accepted'
        return True

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
        return True

    @api.model
    def create(self, vals_list):
        if isinstance(vals_list, dict):
            vals_list = [vals_list]

        for vals in vals_list:
            property = self.env['estate.property'].browse(vals['property_id'])
            if property.offer_ids:
                max_offer_price = max(property.offer_ids.mapped('price'))
                if vals['price'] <= max_offer_price:
                    raise UserError(
                        f"Cannot create an offer lower or equal to existing offers. "
                        f"Current highest offer: {max_offer_price}"
                    )
        offers = super().create(vals_list)
        for offer in offers:
            property = offer.property_id
            if property.state == 'new':
                property.state = 'offer_received'
        return offers

    _check_offer_price_min = models.Constraint(
        "CHECK(price > 0)"
    )
