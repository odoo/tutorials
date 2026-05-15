from odoo import fields,models

class EstateProperty(models.Model):
    _name='estate.property'
    _descripion='Estate Property description modulee'
    name=fields.Char(string='Name',required=True)
    description=fields.Text(string='Description')
    bedrooms=fields.Integer(string='Bedrooms')
    price = fields.Float(string='Price')
    garden = fields.Boolean(string='Garden')
    postcode = fields.Char(string='Postal Code')
    date_available = fields.Date(string='Available Date')
    expected_price = fields.Float(string='Expected Price')
    selling_price = fields.Float(string='Selling Price',required=True)
    meeting_time = fields.Datetime(string='Meeting')
    living_area = fields.Integer(string='Living Area')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation=fields.Selection(
        [
            ('north','North'),('south','South'),('east','East'),('west','West')
        ]
    )

