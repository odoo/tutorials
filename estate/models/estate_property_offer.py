from datetime import datetime, time
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    price = fields.Float(string="Price")
    status = fields.Selection(copy=False,selection = [("Accepted","Accepted"),("Refused","Refused")])
    partner_id = fields.Many2one('res.partner',required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(string="Validity Duration",default=7)
    date_deadline = fields.Date(string="Deadline",compute="_get_date_deadline",inverse="_set_date_deadline")

    def accept_offer(self):
        for record in self:
            if(record.property_id.selling_price == 0):
                record.status = "Accepted";
                print(type(record.property_id.seller_id))
                print(type(record.partner_id))
                record.property_id.buyer_id = record.partner_id;
                record.property_id.selling_price = record.price;
        
        return True;
    
    def refused_offer(self):
        for record in self:
            record.status = "Refused";
        return True;


    @api.depends("validity")
    def _get_date_deadline(self):
        for record in self:
            if(isinstance(record.create_date,bool)):
                record.date_deadline = fields.Datetime.now() + relativedelta(days=record.validity)
                return
            record.date_deadline = record.create_date + relativedelta(days=record.validity)

    def _set_date_deadline(self):
        for record in self:
            record.validity = (datetime.combine(record.date_deadline,time()) - record.create_date).days
