from odoo import fields, models
from datetime import timedelta,datetime

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate App"

    name = fields.Char(required=True)
    description = fields.Text() 
    postcode = fields.Char()
    date_availability = fields.Date(copy=False,default=datetime.now()+timedelta(90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False,readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    is_garage = fields.Boolean()
    is_garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection = [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West'),]
    )
    active=fields.Boolean(default=True)
    state=fields.Selection(
        selection=[('new','New'),('offer_received','Offer Received'),('offer_accepted','Offer Accepted'),('sold','Sold'),('cancelled','Cancelled')]
        ,default='new'
    )
    property_type_id =fields.Many2one("estate.property.type",string="Property Type")
    buyer_id=fields.Many2one("res.partner",string="Buyer", readonly=True)
    seller_id=fields.Many2one("res.users",string="Salesman")
    tag_id=fields.Many2many("estate.property.tag",string="Tags")
    #offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")