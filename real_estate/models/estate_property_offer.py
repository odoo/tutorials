from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float(string="Offer Price")
    state = fields.Selection([
        ('new', 'New'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string="State", default='new', required=True)
    _sql_constraints = [
    ('check_price', 'CHECK(price > 0)', 'The offer price must be strictly positive.'),
]
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    property_type_id = fields.Many2one(
        'estate.property.type',
        related="property_id.property_type_id",
        store=True,
        readonly=True
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Datetime.now()
            record.date_deadline = create_date.date() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Datetime.now()
            delta = record.date_deadline - create_date.date()
            record.validity = delta.days

    def action_accept(self):
        for offer in self:
            if offer.property_id.buyer_id:
                raise UserError("An offer has already been accepted.")
            offer.state = 'accepted'
            offer.property_id.write({
                'selling_price': offer.price,
                'buyer_id': offer.partner_id.id,
                'state': 'offer_accepted'
            })
        return True

    def action_refuse(self):
        for offer in self:
            offer.state = 'refused'
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            price = vals.get('price')
            property_obj = self.env['estate.property'].browse(vals.get('property_id'))
            existing_offers = property_obj.offer_ids.filtered(lambda o: o.price >= price)
            if existing_offers:
                raise ValidationError("You cannot create an offer with a lower or equal price than existing offers.")
            property_obj.state = 'offer_received'

        return super().create(vals_list)
