
from dateutil.relativedelta import relativedelta
from datetime import datetime

from odoo.exceptions import UserError
from odoo import api,fields, models


class EstateOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offers"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection( 
        string = 'Status',
        selection = [('accepted','Accepted'),('refused','Refused')],
        copy = False
    )
    partner_id = fields.Many2one('res.partner',string = "Buyer", required=True)
    property_id = fields.Many2one('estate.property',string="Property", required=True)
    validity = fields.Integer(default = 7)
    date_deadline = fields.Date(compute = '_compute_deadline', inverse = "_inverse_validity", store=True)
    property_type_id = fields.Many2one(related = 'property_id.property_type_id',store= True)

    _sql_constraints = [
        ("offer_price_constraint","CHECK(price > 0)","Offer price should be greater than 0")
    ]

    @api.depends('validity', 'create_date')
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                # print("Hfedfdfdfi", record.id,record.create_date)
                # print(record.create_date.date() + relativedelta(days=record.validity))
                record.date_deadline = record.create_date.date() + relativedelta(days=record.validity)
            else:
                record.date_deadline = datetime.now() + relativedelta(days=record.validity)
        # print(record.create_date, "Hi")

    def _inverse_validity(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_offer_accept(self):
        # print('hi')
        for record in self:
            # accepted_record = False
            # for temp in record.property_id.offer_ids:
            #     if temp.status == 'accepted':
            #         if temp != record:
            #             accepted_record = temp
            #             break

            # if accepted_record != False:
            #     raise UserError("You can not accept two offers at a same time")

            if record.property_id.buyer_id: 
                raise UserError("You can not accept two offers at a same time")
                
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
        return True
    
    def action_offer_refuse(self):
        for record in self:
            offer_list = record.property_id.offer_ids
            for offer in offer_list:
                if offer.status == 'accepted' and offer == record:
                    record.status = 'refused'
                    record.property_id.selling_price = 0
                    record.property_id.buyer_id = False
                    break
            
            record.status = 'refused'
        return True

    @api.model
    def create(self, val):
        property = self.env['estate.property'].browse(val['property_id'])

        max_value = 0
        if(property.offer_ids):
            max_value = max(property.offer_ids.mapped("price"))

        if(val['price'] <= max_value):
            raise UserError('You cant create offer lower than current best offer')
        
        property.state = 'offer_received'
        return super().create(val)
