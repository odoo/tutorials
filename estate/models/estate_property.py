from odoo import models, fields

class EstateProperty(models.Model):

    _name = "estate.property"
    _description = "Damn this model is good for doing real estate related stuff"

    name = fields.Char(required=True)
    description = fields.Text(required = True)
    postcode = fields.Char(required = True)
    date_availability = fields.Date(default = fields.Datetime.now, copy = False)
    expected_price = fields.Float()
    selling_price = fields.Float(readonly = True, copy = False)
    bedrooms = fields.Integer(default = 2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(string='Type',
        selection=[('north', 'North'), ('west', 'West'), ('south', 'South'), ('east', 'East')],
        help="Chose the direct which the garden is facing")
    
    active = fields.Boolean()
    status = fields.Selection(string='Type',
        selection=[('sold', 'Sold'), ('to sell', 'To sell')],
        help="Is the house sold already ?")




