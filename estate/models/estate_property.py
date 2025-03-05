from datetime import date, timedelta
from odoo import models,fields # type: ignore

class estateProperty(models.Model):
    _name ="estate.property"
    _description="estate desccription"

#this is database fields for postgreSql
    name = fields.Char(string="",required =True)
    description = fields.Text(string="Description of property")
    postcode = fields.Char(string="Postcode")

    available_from = fields.Date(
        default=lambda self: date.today() + timedelta(days=90),
        string="Available From",
        copy=False)
    
    expected_price = fields.Float(string="Expected Price")
    selling_price = fields.Float(string="Selling Price",readonly=True,copy=False)
    bedrooms = fields.Integer(string="Bedrooms",default=2)
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden area(sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ('north','North'),
            ('south','South'),
            ('east','East'),
            ('west','West')
        ],
        string="Garden Orientation",
        default="east",
    )
    

    status = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        string="Status",
        required=True,
        default="new",
        copy=False
    )

    active =fields.Boolean(string="Active" ,default = True)



