from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
        ],
        copy=False
    )

    partner_id = fields.Many2one("res.partner", string="Customer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    property_type_id = fields.Many2one(
        related='property_id.property_type',
        string="Property Type",
        store=True
    )

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Datetime.now()
            record.date_deadline = create_date.date() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Datetime.now()
            record.validity = (record.date_deadline - create_date.date()).days

    def action_accept(self):
        for offer in self:
            if offer.property_id.state == 'sold':
                raise UserError("Cannot accept an offer for a sold property.")
            other_offers = offer.property_id.offer_ids.filtered(lambda o: o.id != offer.id)
            other_offers.write({'status': 'refused'})

            offer.status = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer = offer.partner_id
            offer.property_id.state = 'offer_accepted'

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'

    _sql_constraints = [
        ('check_offer_price_positive', 'CHECK(price > 0)',
         'The offer price must be strictly positive.'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get('property_id')
            amount = vals.get('price')
            property = self.env['estate.property'].browse(property_id)
            existing_offers = property.offer_ids.filtered(lambda o: o.price is not None and amount is not None and o.price >= amount)

            if property_id and amount:
                if property.state == 'sold':
                    raise UserError("Cannot create offer for a sold property.")

                if existing_offers:
                    raise ValidationError("An offer with a higher or equal price already exists.")

                if property.state == 'new':
                    property.state = 'offer_received'

        return super().create(vals_list)
