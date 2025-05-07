from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    salesperson_id = fields.Many2one(
        'res.users',
        string='Sales Person',
        default=lambda self: self.env.user,
        required=True
    )

    buyer_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        copy=False
    )

    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string='Offers'
    )

    property_type_id = fields.Many2one('estate.property.type', string="Property Type", required=True)

    tag_ids = fields.Many2many('estate.property.tag', string='Tags')

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string='Available From', copy=False, default=lambda self: fields.Date.today())
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Float(string='Garden Area (sqm)')
    total_area = fields.Float(string='Total Area (sqm)', required=True)
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], string='Garden Orientation')
