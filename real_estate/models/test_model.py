from odoo import fields,models
from datetime import date ,timedelta
class EstateProperty(models.Model):
    _name="estate.property"
    _description="estate.description"
   
    

    name= fields.Char(required=True)
    description=fields.Text()
    expected_price=fields.Float(required=True)
    postcode=fields.Char(required=True)
    date_availability=fields.Date(default=lambda self:date.today()+timedelta(days=90),required=True,copy=False)
    selling_price=fields.Float(copy=False,readonly=True)
    bedrooms=fields.Integer(required=True,default=2)
    living_area=fields.Integer(required=True)
    facades=fields.Integer(required=True)
    garage=fields.Boolean(required=True)
    garden=fields.Boolean(required=True)
    garden_area=fields.Integer(required=True)
    garden_orientation=fields.Selection([
        ('north','North'),('south','South'),('east','East'),('west','West')],string='Garden Orientation'
    )
    
    active=fields.Boolean(default=False)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ], string="Status", required=True, copy=False, default='new')
    # ('option1', 'Label 1')