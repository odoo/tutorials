from odoo import models, api, fields
from datetime import timedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'

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
            # if offer.status != 'pending':
            #     raise UserError("Only pending offers can be accepted.")
            
            existing_offer = self.search([('property_id', '=', offer.property_id.id), ('status', '=', 'accepted')])
            if existing_offer:
                raise UserError("This property already has an accepted offer.")
            # Set the corresponding property fields
            property_record = offer.property_id
            property_record.selling_price = offer.price
            property_record.buyer_id = offer.partner_id
            offer.status = 'accepted'
            property_record.state = 'offer_accepted'  # Change the property state as needed

    def action_refuse_offer(self):
        for offer in self:
            offer.status = 'refused'

    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)

    created_date = fields.Date(default=fields.Date.context_today, string="Created Date")
    validity = fields.Integer(default=7, string="Validity (Days)")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline Date", store="True")

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

    @api.onchange('created_date')
    def _onchange_created_date(self):
        if self.created_date:
            # Recalculate the deadline based on the current validity
            self.date_deadline = self.created_date + timedelta(days=self.validity)

    @api.onchange('validity')
    def _onchange_validity(self):
        if self.created_date:
            # Recalculate the deadline based on the current created date
            self.date_deadline = self.created_date + timedelta(days=self.validity)

    @api.onchange('date_deadline')
    def _onchange_date_deadline(self):
        if self.created_date and self.date_deadline:
            # Recalculate validity based on the created date and new deadline
            self.validity = (self.date_deadline - self.created_date).days

    
        