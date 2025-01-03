from odoo import models,fields,api
from datetime import datetime
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers"

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
            record.property_id.best_price=record.price
            record.property_id.partner_id=record.partner_id

        return True


        
    def cross_refuse(self):
        for record in self:
            record.status='refused'
            
                
            
        return True

    
    
