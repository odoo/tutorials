from odoo import fields, models
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Table"

    name = fields.Char(required=True)
    description = fields.Text('Description', default='bla bla bla')
    postcode = fields.Char('Postcode', default='456010')
    # date_availability = fields.Date()
    date_availability = fields.Date('Availability Date', readonly=False,
                                    copy=False, default=fields.Datetime.today() + relativedelta(days=60))
    expected_price = fields.Float(
        'Expected Price', default='1500000.00', required=True)
    selling_price = fields.Float('Selling Price', default='1500000.00')
    living_area = fields.Integer('Living area', default='15465')
    facades = fields.Integer('Facades', default='4')
    bedroom = fields.Integer('Bedrooms', default='2')
    garage = fields.Boolean('Garage', default=True)
    garden = fields.Boolean('Garden', default=True)
    garden_area = fields.Integer('Garden Area', default='3456', copy=False)
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ], default='north', required=True)
    
    # Chapter 7
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type")
   
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,  # Default is the current user
        required=True
    )

    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False  # Buyer should not be copied
    )

    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers"
    )

    # Reserved field with default value True
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ], copy=False, default='new', required=True)               # Reserved field with default state as New
