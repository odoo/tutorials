from odoo import fields, models, api, exceptions
from dateutil.relativedelta import relativedelta
from datetime import date

class RealEstatePropertyOffer(models.Model):
    _name = 'real.estate.property.offer'
    _description = 'This models is for offer'

    price = fields.Float(string = 'Price')
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        string = 'Status'
    )
    validity = fields.Integer(string = "Validity (days)", default = 7)
    date_deadline = fields.Date(string = "Deadline", default = fields.Datetime.now() + relativedelta(days = 7), inverse = "_inverse_validity", compute = "_compute_deadline")
    partner_id = fields.Many2one('res.partner', required = True, string = 'Partners')
    property_id = fields.Many2one('real.estate.property', required = True, string = 'Property name')
    accept = fields.Boolean(string = "Accept", default = False)
    reject = fields.Boolean(string = "Reject", default = False)

    #date_deadline is automatically calculated 
    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = date.today() + relativedelta(days=record.validity)
    
    #validity is update based on date_deadline when record is saved
    def _inverse_validity(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    #To accept offer
    def action_property_offer_accept(self):
        if self.property_id.status != 'sold':
            if self.property_id.selling_price:
                raise exceptions.UserError("Another offer is already accepted.")
            else:            
                self.status = 'accepted'
                self.property_id.selling_price = self.price
                self.property_id.partner_id = self.partner_id
                self.property_id.status = 'offer_accepted'
        else:
            raise exceptions.UserError("Property already sold.")
        return

    #To reject offer
    def action_property_offer_reject(self):
        if self.status == 'accepted' or self.property_id.status == 'sold':
            self.property_id.status = 'offer_received'

        self.status = 'refused'
        if self.property_id.selling_price:
            self.property_id.selling_price = 0
            self.property_id.partner_id = ''
        return
    
    #Sql constraints to check price
    _sql_constraints = [
        ('check_offers_price', 'CHECK(price >= 0)', 'A property offer price must be strictly positive')
    ]
    