from odoo import models,fields,api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

from odoo.tools import (

    float_compare,
   
)

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers"
    _order= "price desc"

    price = fields.Float('Property Price')
    
    

    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),

        ],
        string='Status',
  
        copy=False,  
    )
    partner_id = fields.Many2one('res.partner', string='Partner',required=True , ondelete="cascade")
    property_id = fields.Many2one('estate.property', string='Property', required=True, ondelete="cascade")


    validity=fields.Integer('Validity (days)', default=7 )
 
    date_deadline=fields.Date('Deadline', compute='_compute_deadline', inverse='_inverse_deadline',default=datetime.today())
    


    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = datetime.today() + relativedelta(days=record.validity)
            print(record.date_deadline , 'this is compute deadline')

    

    
    @api.depends("date_deadline")

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - datetime.today().date()).days
    

    





    def tick_accept(self):
        for record in self:
            record.status='accepted'
            record.property_id.state='offer_accepted'
            record.property_id.selling_price=record.price
            record.property_id.partner_id=record.partner_id

        return True


        
    def cross_refuse(self):
        for record in self:
            record.status='refused'
            
                
            
        return True

    _sql_constraints = [
        (
            "check_offer_price",
            "CHECK(price > 0)",
            "Offer price must be non-negative",
        ),
        
    ]


    # @api.constrains('price','status')
    # def _check_offer_constraint(self):
    #     for record in self:
    #         if record.price < 0.90*record.property_id.expected_price and record.status=='accepted':
    #              raise ValidationError("The selling price must be atleast 90 percentage of expected price")

        
    #     return True



    @api.constrains('price','status')
    def _check_offer_constraint(self):
        for record in self:
            if float_compare(record.price,record.property_id.expected_price*0.9,2)==-1 and record.status=='accepted':
                 raise ValidationError("The selling price must be atleast 90 percentage of expected price")

        
        return True
    

    property_type_id=fields.Many2one(related="property_id.property_type_id")



    @api.model
    def create(self, vals_list):
        
        offer_ref=self.env['estate.property'].browse(vals_list['property_id'])
        if vals_list['price'] < offer_ref.best_price:
            raise UserError("Offer Price must be greater than the best offer price")
        if offer_ref.state=="new":
            offer_ref.state="offer_received"
        

        return super(EstatePropertyOffer, self).create(vals_list)        


    # @api.model_create_multi
    # def create(self, vals_list):
    #     for vals in vals_list:
    #         prop=self.env['estate.property'].browse(vals_list['property_id'])
    #         if vals["price"] < prop.best_price:
    #                 raise UserError('price must be greater than best price')
    #         if prop.state == "new":
    #                 prop.state = "offer_received"
    #     return super().create(vals_list)