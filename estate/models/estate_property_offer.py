from odoo import models, fields, api, exceptions
from datetime import datetime
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = 'price desc'

    price = fields.Float(string="price")
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        copy=False
    )
    partner_id = fields.Many2one('res.partner',required=True)
    property_id = fields.Many2one('estate.property', required=True, ondelete="restrict")
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date( string="Deadline Date", compute="_compute_date_deadline", inverse="_inverse_date_deadline")# default=datetime.today()
    
    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = datetime.today() + relativedelta(
                days=record.validity
            )

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                delta = record.date_deadline - datetime.today().date()
                record.validity = delta.days
            else:
                record.validity = 0

    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)


    def action_confirm(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'offer accepted'

    def action_cancel(self):
        for record in self:
            record.status = 'refused'
    
    @api.model_create_multi             #   Use Decorator Class
    def create(self, vals_list):        #   inherit create method 
        
        for vals in vals_list:
            property_data = self.env['estate.property'].browse(vals['property_id'])     #   Fetch Property data using property_id 
            if vals["price"] < property_data.best_price:                                #   Compare Price with best price
                raise exceptions.UserError("Price can be greater than best price")
            if property_data.state == 'new':                                            #   Change State if it is new Data
                property_data.state = 'offer received'     

        return super().create(vals_list)
    
    _sql_constraints = [
        ('price_positive', 'CHECK(price > 0)', 'The offer price must be strictly positive!')
    ]
    
