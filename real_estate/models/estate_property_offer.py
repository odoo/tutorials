from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers"

    price = fields.Float(required=True)
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        string="Status",
        copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property Name", required=True)
    validity = fields.Integer(string="Valid for", default=7)
    date_deadline = fields.Date(
        string="Offer Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        default=lambda self: date.today() + relativedelta(days=+7)
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        related="property_id.property_type_id",
        store=True
    )

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'The offer price must be greater than 0.'),
        ('check_validity', 'CHECK(validity > 0)', 'The validity must be a positive number.')
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = self.env['estate.property'].browse(vals['property_id'])
            offer_price = vals.get('price')
            existing_offers = property_id.mapped("offer_ids")

            if property_id.status in ('sold', 'offer_accepted'):
                raise ValidationError("Cannot create offer. Property is already sold or has an accepted offer.")

            if existing_offers:
                highest_offer = max(existing_offers, key=lambda o: o.price)
                if offer_price < highest_offer.price:
                    raise ValidationError(
                        f"The offer must be higher than the existing offer of ₹{highest_offer.price:.2f}."
                    )

            property_id.status = "offer_received"

        return super().create(vals_list)

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date.date() if record.create_date else date.today()
            record.date_deadline = base_date + relativedelta(days=+record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            base_date = record.create_date.date() if record.create_date else date.today()
            record.validity = (record.date_deadline - base_date).days

    def accept_offer(self):
        for record in self:
            record.status = "accepted"
            record.property_id.update({
                'selling_price': record.price,
                'buyer_id': record.partner_id.id,
                'status': 'offer_accepted'
            })
            other_offers = record.property_id.offer_ids.filtered(lambda o: o != record)
            other_offers.write({'status': 'refused'})
        return True

    def refuse_offer(self):
        for record in self:
            record.status = "refused"
        return True
