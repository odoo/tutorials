from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import models,fields,api
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError



class test_property_offer(models.Model):
    _name = "test.property.offer"
    _order = "price desc"

    price = fields.Float('price',required=True)
    status = fields.Selection([('Accepted','Accepted'),('Refused','Refused'),('Pennding','pennding')],default="Pennding",copy=False)
    buyer_id = fields.Many2one('res.partner',string='partner_id',required=True)   
    property_id = fields.Many2one('test.property',required=True,ondelete='cascade')
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline',inverse='_inverse_date_deadline',default=datetime.today())
    property_type_id = fields.Many2one(related='property_id.property_types_id',string="property_type")


    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self: 
            record.date_deadline = (datetime.today() +relativedelta(days = record.validity)).date()


    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                record.validity =  (record.date_deadline - datetime.today().date()).days
            else:
                record.date_deadline = 0
    
    def property_accepted(self):
        for record in self:
            if record.property_id.selling_price <= 0:

                if record.status=="Pennding":
                    record.status="Accepted"
                    record.property_id.selling_price = record.price
                    record.property_id.buyer_id = record.buyer_id
                    record.property_id.status = "offer_accepted"

            else:
                raise UserError(" offer already accepted")


    def property_rejected(self):
        for record in self:
            if record.status=="Accepted" or record.status=="Pennding":
                record.status="Refused"
                record.property_id.selling_price = 0
                record.property_id.status = "offer_received"

            else:
                record.status="Pennding"


    @api.constrains('price','status')
    def _check_offer_constraint(self):
        for record in self:
            if  (record.price / record.property_id.expected_price * 100)  < 90 and record.status=='Accepted':
                 raise ValidationError("The selling price must be atleast 90 percentage of expected price")


        return True










