from dateutil.relativedelta import relativedelta

from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Handle real estate property"

    name = fields.Char(string='Title', required=True)
    description = fields.Text()
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Available From', copy=False, default=fields.Date.today()+ relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string = 'Status',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), 
                    ('offer_accepted', 'Offer accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        required = True,
        copy=False,
        default='new'
    )

    property_type_id = fields.Many2one('estate.property.type')
    buyer_id = fields.Many2one('res.partner', copy=False)
    salesman_id = fields.Many2one('res.users', default=lambda self: self.env.user) 
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
