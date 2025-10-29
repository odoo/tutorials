from datetime import timedelta
from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"
    _sql_constraints = [
        ('check_offer_price_positive', 'CHECK(price > 0)', 'Offer price must be strictly positive.')
    ]

    price = fields.Float(required=True)
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ])
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", required=True, ondelete='cascade')
    property_type_id = fields.Many2one(related="property_id.property_type", store=True, string="Property Type")
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline Date", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - create_date).days

    def action_accept(self):
        for record in self:
            if record.property_id.state == 'sold':
                raise UserError("You cannot accept an offer on a sold property.")
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer = record.partner_id
            record.property_id.state = 'offer_accepted'
            other_offers = self.search([
                ('property_id', '=', record.property_id.id),
                ('id', '!=', record.id)
            ])
            other_offers.write({'status': 'refused'})

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            price = vals.get('price')
            property_id = vals.get('property_id')
            if not property_id:
                raise ValidationError("Property ID must be provided.")
            property_obj = self.env['estate.property'].browse(property_id)

            if property_obj.state == 'sold':
                raise UserError("Cannot create offer for a sold property.")
            existing_offers = property_obj.offer_ids.filtered(
                lambda o: o.price is not None and price is not None and o.price >= price
            )
            if existing_offers:
                raise ValidationError("You cannot create an offer with a lower or equal price than existing offers.")
            property_obj.state = 'offer_received'
        return super().create(vals_list)
