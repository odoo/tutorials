from datetime import timedelta

from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection([
        ('new', 'New'), 
        ('offer received', 'Offer Received'), 
        ('offer accepted', 'Offer Accepted'), 
        ('sold', 'Sold'), 
        ('cancelled', 'Cancelled')
        ], default="new", string="State"
    )
    last_seen = fields.Datetime(string="Last Seen", default=fields.Datetime.now)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available from", copy=False, default=fields.Date.today() + timedelta(days=+90))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False) 
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection([
        ('north', 'North'), 
        ('south', 'South'), 
        ('east', 'East'), 
        ('west', 'West')
        ], string="Garden Orientation", help="Orientation of the garden"
    )   
    property_type = fields.Many2one(comodel_name="estate.property.type", string="Property Type")
    buyer = fields.Many2one(comodel_name="res.partner", string="Buyer", copy=False)
    seller = fields.Many2one(comodel_name="res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many(comodel_name="estate.property.tag", string="Tags")
    offer_ids = fields.One2many(comodel_name="estate.property.offer", inverse_name="property_id", string="Offers"
    )
