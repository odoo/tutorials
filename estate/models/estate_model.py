from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Brand new Model"

    name = fields.Char(required=True, default="Unknown")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[
        ('N', 'North'),
        ('S', 'South'),
        ('E', 'East'),
        ('W', 'West')
    ])
    active = fields.Boolean(default=False)
    state = fields.Selection(selection=[
        ('N', 'New'),
        ('OR', 'Offer Received'),
        ('OA', 'Offer Accepted'),
        ('S', 'Sold'),
        ('C', 'Canceled')
    ], required=True, copy=False, default='N')
    