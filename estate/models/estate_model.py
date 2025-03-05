from odoo import models, fields
from datetime import timedelta

class estateModel(models.Model):
    _name = "estate_model"
    _description = "Estate model help save data"
    
    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date('Availability From', default=lambda self: fields.Date.today()+timedelta(days=90),copy=False)
    expected_price = fields.Float(required = True)
    selling_price = fields.Float('Selling Price', readonly=True,copy=False)
    bedrooms = fields.Integer('Number of Bedrooms', default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    
   
    lead_type = fields.Selection(
        string='Type',
        selection=[('lead', 'Lead'), ('opportunity', 'Opportunity')],
        help="Type is used to separate Leads and Opportunities")

    active = fields.Boolean('Active', default= True)

    state = fields.Selection(
        string='State',
        selection=[
         ('new', 'New'),
         ('offer_received', 'Offer Received'),
         ('offer_accepted', 'Offer Accepted'),
         ('sold', 'Sold'),
         ('cancelled', 'Cancelled'),
        ] , default = 'new', copy = False , required= True
    )   