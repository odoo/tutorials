from odoo import models, fields

class MyModel(models.Model):
    _name = 'estate_property'
    _description = 'Real Estate'

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Available From')
    expected_price = fields.Float(string='Expected Price')
    selling_price = fields.Float(string='Selling Price')
    bedrooms = fields.Integer(string='Bedrooms')
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'), 
            ('south', 'South'), 
            ('east', 'East'), 
            ('west', 'West')],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(string='Status',
        selection=[
            ('new', 'New'), 
            ('offer received', 'Offer Received'), 
            ('offer accepted', 'Offer Accepted'), 
            ('sold', 'Sold'), 
            ('canceled', 'Canceled')],
        default='new'
    )
    salesman_id = fields.Many2one(
        'res.users',          # The model this field relates to
        string='Salesman',    # Label for the field
        default=lambda self: self.env.user # Set default to the current user
    )
    buyer_id = fields.Many2one(
        'res.partner',        # The model this field relates to
        string='Buyer',       # Label for the field
        copy=False            # Prevent the field value from being copied when duplicating the record
    )

    tag_ids = fields.Many2many('real.estate.property.tag', string='tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
