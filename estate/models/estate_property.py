from odoo import fields, models


class EstateModel(models.Model):
    _name = 'estate.property'
    _description = 'Estate properties'

    name = fields.Char('Title', required=True, translate=True)
    description = fields.Text()
    postcode = fields.Integer(help='Your post code in 4 or 5 digits. e.g: 3000')
    date_availability = fields.Date('Available From', copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (m²)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer('Garden Area (m²)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('west', 'West'), ('south', 'South'), ('east', 'East')],
        help='The selection of the garden orientation.')
    active = fields.Boolean(default=True)
    state = fields.Selection(
        required=True,
        copy=False,
        default='new',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')])
