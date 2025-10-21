from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Table that stores the estate properties"


    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()

    date_availability = fields.Date(
        string="Available From", 
        copy=False, 
        default=lambda self: fields.Date.add(fields.Date.today(), months=3)
    )

    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=False, copy=False)

    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()

    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'), 
            ('south', 'South'), 
            ('east', 'East'), 
            ('west', 'West')
        ]
    )

    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'), 
            ('offer', 'Offer'), 
            ('received', 'Received'), 
            ('accepted', 'Accepted')
        ]
    )