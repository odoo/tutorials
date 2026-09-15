from odoo import models, fields


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate property model'

    name = fields.Char('Name',required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode',required=True)
    date_availability = fields.Date('Availability',copy=False,default=fields.Date.add(fields.Date.today(),months=3))
    expected_price = fields.Float('Expected Price',required=True)
    selling_price = fields.Float('Selling Price',readonly=True,copy=False)
    bedrooms = fields.Integer('Bedrooms',default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('North','North'),('South','South'),('East','East'),('West','West')]
    )
    active = fields.Boolean('Active',default=True)
    state = fields.Selection(
        string='State',
        selection=[('New','New'),('Offer Received','Offer Received'),
                   ('Offer accepted','Offer accepted'),('Sold','Sold'),('Cancelled','Cancelled')],
        required=True,
        copy=False,
        default='New'
    )


