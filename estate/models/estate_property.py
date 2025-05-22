from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "real estate properties"

    name = fields.Char('Title', default="Unknown", required=True)
    description = fields.Char('Descrption')
    postcode = fields.Char('Postcode', required=True, default='00000')

    availability_date = fields.Date('Availability', copy=False)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2, required=True)
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    expected_price = fields.Float('Expected Price', required=True)
    living_area = fields.Float('Living Area (sqm)', required=True, default=20.0)
    facades = fields.Integer('Facades', required=True)
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('west', 'West'),
            ('east', 'East'),
            ('south', 'South'),
        ],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='Property State',
        selection=[
            ('new', 'New'),
            ('offer Received', 'Offer Received'),
            ('offer Accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
    )
    Property_type_id = fields.Many2one('estate.property.type', 'Property Type')
    partner_id = fields.Many2one('res.partner', 'Partner')
    seller_id = fields.Many2one('res.users', 'Salesperson', default=lambda self: self.env.user)