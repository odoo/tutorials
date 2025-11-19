from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate properties"

    name = fields.Char('Name', required=True, translate=True)
    description = fields.Text('Description', required=True)
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available From', copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float('Expected Price')
    selling_price = fields.Float('Selling Price', readonly=True)
    bedrooms = fields.Integer(default=2)
    active = fields.Boolean(default=True)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Float('Garden Area (sqm)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    state = fields.Selection(
        string='State',
        required=True,
        default='new',
        copy=False,
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')])
    property_type_id = fields.Many2one("estate.property.type", "Type")
