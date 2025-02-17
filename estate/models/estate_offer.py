from dateutil.relativedelta import relativedelta
from datetime import datetime

from odoo import models, fields, api
from odoo.exceptions import UserError,ValidationError

class EstateOffer(models.Model):
    _name = 'estate.property.offer' 
    _description = 'Offer'
    _order = "id desc"

    price = fields.Float(string="Price", required=True)
    status_offer = fields.Selection([
        ('new', 'New'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string="Status", default='new', copy=False)  

    partner_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    property_id = fields.Many2one('estate.property', string="Property", required=True,ondelete='cascade')
    property_type_id=fields.Many2one('estate.property.type',related='property_id.property_type_id',store=True)

    validity = fields.Integer(string="Validity (Days)", store=True)
    date_deadline = fields.Date(string="Date-Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    _sql_constraints = [
            ("check_offer_price", "CHECK (price > 0)", "Offer price should strictly be positive")
        ]

    @api.constrains('price')
    def _check_price(self):
        for record in self:
            if record.price<=0:
                raise ValidationError("price should strictly be positive")



    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        """ Compute date_deadline based on create_date and validity. """
        for record in self:
            # added fallback
            start_date = record.create_date if record.create_date else datetime.now() #if create_date is not there then it will be calculate based on the current date.
            if start_date and record.validity:
                record.date_deadline = start_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        """ Inverse function to set validity based on date_deadline """
        for record in self:
            if record.date_deadline and record.create_date:
                delta = record.date_deadline - record.create_date.date()
                record.validity = delta.days
            else:
                record.validity = 7  # Default validity if no date_deadline is set

    def accept_offer(self):
        """ Accept an offer """
        for record in self:
            record.status_offer = "accepted"
            record.property_id.selling_price=record.price
            record.property_id.property_buyer_id=record.partner_id
            record.property_id.status="offer_accepted"
        return True

    def reject_offer(self):
        """ Reject an offer """
        for record in self:
            record.status_offer = "refused"
            record.property_id.selling_price=0.000
        return True

    @api.model
    def create(self, vals):
        # Step 1: Set the property state to 'Offer Received' when a new offer is created
        property_id = vals.get('property_id')
        if property_id:
            property_record = self.env['estate.property'].browse(property_id)
            if property_record:
                # Update the property status to 'offer_received'
                if(property_record.status=="sold"):
                    raise UserError("Can not create offer for sold property")
                property_record.write({'status': 'offer_received'})

        # Step 2: Raise an error if the new offer price is lower than an existing offer
        if vals.get('price') is not None:
            existing_offers = self.env['estate.property.offer'].search([
                ('property_id', '=', vals.get('property_id'))
            ])
            highest_offer = max(existing_offers.mapped('price'), default=0)
            if vals['price'] < highest_offer:
                raise UserError(f"The offer price must be higher than the existing offer of {highest_offer}.")
        
        # Call the super class to create the record
        return super().create(vals)


