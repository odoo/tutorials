from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Property estates"

    state = fields.Selection(
        string='Type',
        selection=[('New', 'New'), ('Offer_Received', 'Offer Received'), ('Offer_Accepted', 'Offer Accepted'), ('Sold', 'Sold'), ('Canceled', 'Canceled')],
    )
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, 
        default=fields.Date.add(fields.Date.today(), months=3) # default 3 months from now
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Type',
        selection=[('North', 'North'), ('East', 'East'), ('South', 'South'), ('West', 'West')],
    )
    active = fields.Boolean(default=True)
