from odoo import fields, models
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate properties"

    name = fields.Char('Title', required=True, translate=True)
    tags_ids = fields.Many2many('estate.property.tag', string='Tags')
    property_type = fields.Many2one('estate.property.type', string='Property Type')
    salesman = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', string='Buyer', copy=False)
    offer_id = fields.One2many('estate.property.offer', 'property_id')  # we have give the Many2one field defined in the comodel in the One2many field, because One2many relationship is virtual, it only exist when corrensponding Many2one field exist in the comodel.
    description = fields.Text('Description')
    postcode = fields.Char('Postcode', required=True)
    date_availability = fields.Date('Available From', copy=False, default=fields.Datetime.today() + relativedelta(months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selleing Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default="2")
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')],
        help="Defines the orientation of the garden")
    active = fields.Boolean('Active', default="True")
    state = fields.Selection(
        string='Status',
        selection=[('new', 'New'),
        ('offer received', 'Offer Received'),
        ('offer accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')],
        help="Status of the Property",
        required=True,
        copy=False,
        default="new")
