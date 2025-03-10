from odoo import fields, models, api, exceptions
from dateutil.relativedelta import relativedelta
from datetime import date

class RealEstatePropertyOffer(models.Model):
    _name = 'real.estate.property.offer'
    _description = 'This models is for offer'
    _order = "price desc"

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
    property_type_id = fields.Many2one(related = "property_id.property_type_id", string="Property Type", store = True)

    #Sql constraints to check price
    _sql_constraints = [
        ('check_offers_price', 'CHECK(price >= 0)', 'A property offer price must be strictly positive')
    ]

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
        self.status = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.partner_id = self.partner_id
        self.property_id.status = 'offer_accepted'
        for record in self.property_id.offer_ids:
            if self != record:
                record.status = 'refused'
        return

    #To reject offer
    def action_property_offer_reject(self):
        self.status = 'refused'
        return
