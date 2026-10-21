from odoo import fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Properties'

    name = fields.Char('Estate Property', required=True, translate=True)
    description = fields.Char('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available from', default=lambda self: fields.Date.add(fields.Date.today(), months=3), copy=False)
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Façades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Oriented is used to show which cardinal direction the garden is oriented to",
    )
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('received', 'Offer Received'), ('accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        required=True,
        default='new',
        copy=False,
        help="Shows the state of the property",
    )
    property_type_id = fields.Many2one('estate.property.type', string='Type')
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
