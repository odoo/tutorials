from odoo import models, fields
from datetime import date, timedelta 
from odoo import api

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    active = fields.Boolean(default=True)

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")

    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user
    )

    buyer_id = fields.Many2one(
         "res.partner",
         string="Buyer",
         copy=False
    )

    tag_ids = fields.Many2many(
         "estate.property.tag",
         string="Tags"
    )

    state = fields.Selection(
        [
            ('new', 'New'), 
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
    )

    expected_price = fields.Float(string="Expected Price")

    selling_price = fields.Float(
        string="Selling Price",
        readonly=True,  
        copy=False     
    )

    bedrooms = fields.Integer(
        string="Bedrooms",
        default=2  
    )

    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Number of Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")

    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string="Garden Orientation"
    )

    postcode = fields.Char(string="Postcode")

    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: date.today() + timedelta(days=90) 
    )
