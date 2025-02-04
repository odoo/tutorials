from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, exceptions, fields, models


class EstatepropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'RealEstate Model'
    _order = 'price desc'

    price = fields.Float(required=True,string='Price')
    status = fields.Selection(
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused")
        ],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(string='Validity(day)', default='7')
    date_deadline = fields.Date(string='Date Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one('estate.property.type', related='property_id.property_type_id', string="Property Type", store=True)

    #---------------------------
        #Compute Methods
    #---------------------------

    @api.depends('property_id', 'validity')
    def _compute_date_deadline(self):
        for records in self:
            if records.validity:
                if records.create_date:
                    records.date_deadline = fields.Date.add(records.create_date, days=records.validity)
                else:
                    records.date_deadline = fields.Date.add(datetime.today(), days=records.validity)

    @api.depends('date_deadline')
    def _inverse_date_deadline(self):
        for records in self:
            records.validity = (records.date_deadline - records.create_date).days 

    #---------------------------
        #Contrains Methods
    #---------------------------

    @api.constrains('price')
    def _check_price(self):
        if any(self.filtered(lambda offer: offer.price < 0)):
            raise exceptions.ValidationError("Offer Price must be positive.")

    #------------------------
        #CRUD Methods
    #------------------------

    @api.model_create_multi
    def create(self, vals_list):
        res = []
        for vals in vals_list:
            property_id = vals.get('property_id')
            new_offer_price = vals.get('price')
            if property_id:
                property = self.env['estate.property'].browse(property_id)

                if property.state in ['sold', 'cancelled', 'offer_accepted']:
                    raise exceptions.UserError("You can add offer in New or Offer Received state only")

                existing_offer = self.search([('property_id', '=', property_id), ('price', '>=', new_offer_price)])
                if existing_offer:
                    raise exceptions.UserError("Already Higher offer exist, Increase your offer price")
                property.state = 'offer_received'
                res.append(super(EstatepropertyOffer, self).create(vals))
        return res

    #---------------------------------
        #Actions methods
    #---------------------------------

    def action_accept(self):
        if self.property_id.state == 'sold':
            raise exceptions.UserError("Sold Property can not accept any offers")
        elif self.property_id.state == 'cancelled':
            raise exceptions.UserError("Cancelled Property can not accept any offers")
        elif self.status == 'accepted':
            raise exceptions.UserError("Offer is already accepted")
        else:
            self.status = 'accepted'
            self.property_id.state = 'offer_accepted'

            for offer in self.property_id.offer_ids:
                if offer.id != self.id:
                    offer.status = 'refused'
                else:
                    offer.property_id.write({'buyer_id' : offer.partner_id, 'selling_price' : offer.price})

    def action_refuse(self):
        if self.property_id.state == 'sold':
            raise exceptions.UserError("Sold Property can not refuse any offers")
        elif self.property_id.state == 'cancelled':
            raise exceptions.UserError("Cancelled Property can not refuse any offers")
        elif self.status == 'refused':
            raise exceptions.UserError("Offer is already refuse")
        self.status = 'refused'
