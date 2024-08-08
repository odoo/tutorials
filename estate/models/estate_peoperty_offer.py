from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property offer'
    _order = 'price desc'
    price = fields.Float('Price')
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string='Status', copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer('Validity', default=7)
    date_deadline = fields.Date('Deadline_of_Offer', compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one(
        related='property_id.property_type_id',
        store=True,
        string='Property Type'
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                create_date = fields.Date.from_string(record.create_date)
                record.date_deadline = create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                create_date = fields.Date.from_string(offer.create_date)
                if create_date:
                    offer.validity = (fields.Date.from_string(offer.date_deadline) - create_date).days
                else:
                    offer.validity = 7
            else:
                offer.validity = 7

    def action_accept(self):
        for offer in self:
            if offer.property_id.state in ['sold', 'canceled']:
                raise UserError("Cannot accept an offer for a sold or canceled property.")
            existing_accepted_offer = self.env['estate.property.offer'].search([
                ('property_id', '=', offer.property_id.id),
                ('status', '=', 'accepted')
            ], limit=1)
            if existing_accepted_offer:
                raise UserError("An offer has already been accepted for this property.")
            offer.status = 'accepted'
            offer.property_id.state = 'offer_accepted'
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            other_offers = self.env['estate.property.offer'].search([
                ('property_id', '=', offer.property_id.id),
                ('id', '!=', offer.id)
            ])
            other_offers.write({'status': 'refused'})

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
        return True

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price >= 0)', 'An offer price must be strictly positive')
    ]

    @api.constrains('price')
    def _check_offer_price(self):
        for record in self:
            if record.price <= 0:
                raise ValidationError("Price must be strictly positive.")
