from odoo import fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Post Code')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')

    date_availability = fields.Date('Availability Date', copy=False,
        default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)

    bedrooms = fields.Integer('# Bedrooms', default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('# Facades')
    garage = fields.Boolean('Garage')

    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'), ('south', 'South'),
            ('east', 'East'), ('west', 'West')
        ])

    user_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.uid)
    partner_id = fields.Many2one('res.partner', string='Buyer', copy=False)

    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'), ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        default='new',
        required=True
    )
