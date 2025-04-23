from odoo import fields,models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Properties of an estate"
    

    name = fields.Char('Title',required=True, translate=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date Availability', copy=False, default=fields.Date.add(fields.Date.today(),months=3))
    expected_price = fields.Float('Expected Price',required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms',default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(string='Orientation Type', selection=[('north', 'North'), ('south', 'South'),('west', 'West'), ('east', 'East')])
    active = fields.Boolean(default=True)
    state = fields.Selection(required=True, copy=False, default='New', selection=[('New', 'New'), ('Offer Received', 'Offer Received'),('Offer Accepted', 'Offer Accepted'), ('Sold', 'Sold'), ('Cancelled', 'Cancelled')])