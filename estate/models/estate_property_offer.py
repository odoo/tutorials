from odoo import fields, models, api, _ #importing _ for the text of the error(unsure).
from odoo.exceptions import ValidationError, UserError #importing to throw error in ui view
from dateutil.relativedelta import relativedelta 
from datetime import datetime

class EstatePropertyOffer(models.Model):
    _name= "estate.property.offer"
    _description= "offer going to apply on a property"
    
    price= fields.Float(string="Price")
    status= fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')    
        ],
        copy=False,
        help="Status of the offer"
    )
    partner_id= fields.Many2one(comodel_name="res.partner", required=True) #jha many2one hai fk vha store hoga
    property_id= fields.Many2one(comodel_name="estate.property", required=True) #! define the one2many field, including comodel & inverse_name in the foreign table as wel
    
    validity= fields.Integer(string="Validity", default=7)
    
    #=====================================================================================#
    
    _sql_constraints= [
        ('check_price','CHECK(price>0)','Price cannot be a negative value')
    ]
    
    #=====================================================================================#
    #! if we do no define the inverse the date_deadline field stays non editable, inverse property let user choose the date_deadline and doing so will update the validity time on save of the record.
    date_deadline= fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline",help="today date + validity")
    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self: #runs everytime in the list view
            if(record.create_date is None or record.create_date is False): #Fallback if create_date is None take today date and update deadline
                record.date_deadline= fields.Date.today() + relativedelta(days=+record.validity)
            else:
                record.date_deadline= record.create_date + relativedelta(days=+record.validity)
                
    @api.depends('validity', 'date_deadline')
    def _inverse_date_deadline(self):
        for record in self:
            if(record.create_date is None or record.create_date is False):
                record.validity= 7
            else:
                start_date = record.create_date
                end_date = record.date_deadline
                d1 = datetime.strptime(str(start_date), '%Y-%m-%d %H:%M:%S.%f')
                d2 = datetime.strptime(str(end_date), '%Y-%m-%d')
                date_difference = d2 - d1
                
                if(date_difference.days<0):
                    raise ValidationError(_("deadline can only be in future"))
                record.validity=  date_difference.days
                
    def mark_offer_accept(self):
        for record in self:
            if(record.property_id.selling_price!=0.0):
                raise UserError(_("Only One offer can be accepted for a given property."))

            record.status= 'accepted'
            record.property_id.selling_price=record.price
            record.property_id.buyer= record.partner_id
        return True
        
    #an accepted offer can be rejected by setting selling_price to 0.0 and then status=refused
    def mark_offer_refuse(self):
        for record in self:
            record.status= 'refused'
        return True