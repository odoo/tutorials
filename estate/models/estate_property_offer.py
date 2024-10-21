from datetime import timedelta

from odoo.exceptions import UserError #type: ignore
from odoo import api, fields, models #type: ignore


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'
    _order = "price desc" 

    price = fields.Float(required=True)
    _sql_constraints = [
        ('check_offer_price_positive', 'CHECK(price > 0)', 'Offer price must be strictly positive.'),
        ]

    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
        ('pending', 'Pending'),
    ])

    def action_accept_offer(self):
        for offer in self:
            existing_offer = self.search([('property_id', '=', offer.property_id.id), ('status', '=', 'accepted')])
            if existing_offer:
                raise UserError("This property already has an accepted offer.")
            property_record = offer.property_id
            property_record.selling_price = offer.price
            property_record.buyer_id = offer.partner_id
            offer.status = 'accepted'
            property_record.state = 'offer_accepted'

    def action_refuse_offer(self):
        for offer in self:
            offer.status = 'refused'
            self.property_id.selling_price = 0

    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True, string="Property Type")
    created_date = fields.Date(default=fields.Date.context_today, string="Created Date")
    validity = fields.Integer(default=7, string="Validity (Days)")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline Date", store="True") #inverse="_inverse_date_deadline"

    @api.depends('created_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.created_date and record.validity:
                record.date_deadline = record.created_date + timedelta(days=record.validity)
            else:
                record.date_deadline = False

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.created_date:
                record.validity = (record.date_deadline - record.created_date).days
            else:
                record.validity = 0

    # @api.onchange('created_date')
    # def _onchange_created_date(self):
    #     if self.created_date:
    #         # Recalculate the deadline based on the current validity
    #         self.date_deadline = self.created_date + timedelta(days=self.validity)

    # @api.onchange('validity')
    # def _onchange_validity(self):
    #     if self.created_date:
    #         # Recalculate the deadline based on the current created date
    #         self.date_deadline = self.created_date + timedelta(days=self.validity)

    # @api.onchange('date_deadline')
    # def _onchange_date_deadline(self):
    #     if self.created_date and self.date_deadline:
    #         # Recalculate validity based on the created date and new deadline
    #         self.validity = (self.date_deadline - self.created_date).days


    @api.model
    def create(self, vals):
        property = self.env['estate.property'].browse(vals.get('property_id'))
        if property and property.best_price:
            if vals.get('price', 0) <= property.best_price:
                raise UserError('Offer price must be higher than the best offer price for this property.')
        property.state = "offer_received" 
        return super(EstatePropertyOffer, self).create(vals)
     