from odoo import models, fields
from datetime import timedelta, date

class EstateProperty(models.Model):

    _name = 'estate.property'

    _description = 'Real Estate Property'

    active = fields.Boolean(string="active",default=True)

    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ], default='new', required=True, copy=False)

    name = fields.Char(string="Property Name", required=True) 

    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    sales_man = fields.Many2one('res.partner', string="Salesman",default=lambda self: self.env.user)
    buyer = fields.Many2one('res.users', string="Buyer")

    description = fields.Text(string="Description")

    selling_price = fields.Float(readonly=True, copy=False)

    postcode = fields.Char(string="Postcode")

    availability_date = fields.Date(string="availability_date",default=lambda self: date.today() + timedelta(days=90),copy=False)

    expected_price = fields.Float(string="Expected Price", required=True)

    selling_price = fields.Float(string="Selling Price")

    bedrooms = fields.Integer(string="Number of Bedrooms",default=2)

    living_area = fields.Integer(string="Living Area (sqm)")

    facades = fields.Integer(string="Number of Facades")

    garage = fields.Boolean(string="Garage")

    garden = fields.Boolean(string="Garden")

    garden_area = fields.Integer(string="Garden Area (sqm)")

    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orientation"
    )

    tag_ids = fields.Many2many('estate.property.tag',string='Tags')

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Property Offers')




