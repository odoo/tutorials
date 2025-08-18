from odoo import fields, models
from datetime import timedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    def _default_availability_date(self):
        today_str = fields.Date.context_today(self) 
        today_date = fields.Date.to_date(today_str)   
        future_date = today_date + timedelta(days=30)
        return future_date.strftime('%Y-%m-%d')   

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availaility = fields.Date(copy=False,default=_default_availability_date)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly = True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string = 'Type',
        selection=[('North','north'),('South','south'),('East','east'),('West','west')],
        help="Type is used to know the direction of the Garden ")
    active = fields.Boolean(default = True)
    state = fields.Selection([   ('new', 'New'),
    ('offer_received', 'Offer Received'),
    ('offer_accepted', 'Offer Accepted'),
    ('sold', 'Sold'),
    ('cancelled', 'Cancelled'),],required=True, copy=False, default='new')





