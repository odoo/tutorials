from datetime import timedelta
from odoo import models, fields

class EstateProperty(models.Model):
    _name ="estate.property"
    _description="test description"


    name=fields.Char(required=True,default="Unknown")
    description=fields.Text()
    postcode=fields.Char()
    date_availability=fields.Date(copy=False,default=fields.Date.today()+timedelta(days=+90))
    expected_price=fields.Float(required=True)
    selling_price=fields.Float(readonly=True, copy=False)
    bedrooms=fields.Integer(default=2)
    living_area=fields.Integer()
    facades=fields.Integer()
    garage=fields.Boolean()
    garden=fields.Boolean()
    garden_area=fields.Integer()
    garden_orientation=fields.Selection(
        string='Garden Orientation',
        selection=[('north','North'), ('south','South'), ('east','East'), ('west','West'),],
        help="It is used to define the garden orientation"
    )
    state=fields.Selection(
        default="new",
        selection=[('new', 'New'), ('offerreceived', 'Offer Received'), ('offeraccepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')]
    )
    active=fields.Boolean(default=True)