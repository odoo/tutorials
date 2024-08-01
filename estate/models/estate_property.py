from odoo import models, fields


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    Title = fields.Char(required=True)
    Description = fields.Text()
    Postcode = fields.Char()
    Availability_date = fields.Date(copy=False)
    Expected_price = fields.Float(required=True, default=0.0)
    Selling_price = fields.Float(string="Selling Price", readonly=True)
    Bedrooms = fields.Integer(default=2)
    Living_area = fields.Integer()
    Facades = fields.Integer()
    Garage = fields.Boolean()
    Garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    state = fields.Selection([
        ('new', 'New'),
        ('used', 'Used'),
    ], string='Status', default='new')
    active = fields.Boolean(string='Active', default=True)
