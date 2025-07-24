from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate_property_offer"
    name = fields.Char(required = True)
    price = fields.Float()
    state = fields.Selection(
        string='State',
        selection=[('Accepted', 'Accepted'),('Refused','Refused')],
        copy = False)
    partner_id = fields.Many2one('res.partner', string='Partner',required = True)
    property_id = fields.Many2one('estate_property',required = True)
    date_deadline = fields.Date(compute = '_compute_deadline', inverse = '_compute_validity')
    validity = fields.Integer(default = 7)
    @api.depends('validity')
    def _compute_deadline(self):
        for property in self:
            if not property.create_date:
                property.date_deadline = fields.Date.add(fields.Date.today(), days = property.validity)

            else:
                property.date_deadline = fields.Date.add(property.create_date, days = property.validity)


    

    def _compute_validity(self):
        for property in self:
            if not property.create_date:
                
                property.validity = (property.date_deadline - fields.Date.today()).days
                

            else:
                property.validity = (datetime.combine(property.date_deadline, datetime.min.time()) - property.create_date).days



    
    def action_confirm(self):
        for record in self:
            if record.property_id.state not in ["Cancelled", "Sold", "Offer Accepted"]:
                record.state = 'Accepted'
                record.property_id.buyer = record.partner_id
                record.property_id.selling_price = record.price
                record.property_id.state = "Offer Accepted"
            elif record.property_id.state ==  "Offer Accepted":
                if record.state != "Accepted":
                    raise UserError("Only one offer can be accepted!")

            else:
                raise UserError("Property not available!")
            
        return True



    def action_reject(self):
        for record in self:
            if record.property_id.state not in ["Cancelled", "Sold"]:
                if record.state == 'Accepted':
                    record.property_id.state = "New"
                    record.property_id.buyer = ''
                    record.property_id.selling_price = 0.0
                record.state = 'Refused'

            else:
                raise UserError("Property not available!")
            
            

        return True


    _sql_constraints = [
        ('strictly_positive_offer_price', 
        'CHECK(price > 0)',
         'The offer price should be strictly positive')

    ]