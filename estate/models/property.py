from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = 'estate_property'
    _description = 'estate property'

    name = fields.Char(string='Title', required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string='Available From', copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection(selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')], required=True, copy=False, default='new')

    property_type_id = fields.Many2one('estate_property_type', string='Property Type')

    salesperson = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', copy=False)

    property_tag_id = fields.Many2many('estate_property_tag', string='Property Tag')

    property_offer_id = fields.One2many('estate_property_offer', 'property_id', string='Property Offer')

    total_area = fields.Float(string="Total Area (sqm)", compute='_compute_area')

    @api.depends('living_area', 'garden_area')
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_price = fields.Float(string="Best offer", compute='_compute_best_price')

    @api.depends('property_offer_id.price')
    def _compute_best_price(self):
        best_price_compute = max(self.mapped('property_offer_id.price'), default=0)
        for record in self:
            record.best_price = best_price_compute
