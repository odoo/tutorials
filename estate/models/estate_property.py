from odoo import fields, models

class EstatePropertyModel(models.Model):
    _name = "estate.property"
    _description = "Estate Property"


    title = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availablility = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('EAST','East'),('WEST','West'), ('SOUTH','South'), ('NORTH','North')])
    state = fields.Selection([("NEW","New"), ("OFFER_RECEIVED","Offer Received"), ("OFFER_ACCEPTED","Offer Accepted"), ("SOLD","Sold"), ("CANCELLED","Cancelled")], required=True)
    