from odoo import _, api, fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char(
        string='Name',
        required=True,
        default="Unknown",
    )
    description = fields.Text(
        string='Description',
    )
    postcode = fields.Char(
        string='Postcode',
    )
    date_availability = fields.Date(
        string='Date availability',
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(
        string='Expected price',
        required=True,
    )
    selling_price = fields.Float(
        string='Selling price',
        readonly=True,
        copy=False,
    )
    bedrooms = fields.Integer(
        string='Bedrooms',
        default=2,
    )
    living_area = fields.Integer(
        string='Living area',
    )
    facades = fields.Integer(
        string='Facades',
    )
    garage = fields.Boolean(
        string='Garage',
    )
    garden = fields.Boolean(
        string='Garden',
    )
    garden_area = fields.Integer(
        string='Garden area',
    )
    garden_orientation = fields.Selection(
        string='Garden orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('offer_received', 'Offer received'), ('offer_accepted', 'Offer accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        required=True,
        copy=True,
        default='new',
    )
    property_type = fields.Many2one(
        comodel_name='estate_property_type',
        string='Property type',
    )
    buyer = fields.Many2one(
        comodel_name='res.partner',
        string='Buyer',
        copy=False,
    )
    salesperson = fields.Many2one(
        comodel_name='res.users',
        string='Salesperson',
        default=lambda self: self.env.user,
    )
    tags = fields.Many2many(
        comodel_name='estate_property_tag',
        string='Tags',
    )
    offers = fields.One2many(
        comodel_name='estate_property_offer',
        inverse_name='property_id',
        string='Offers',
    )
    total_area = fields.Integer(
        compute='_compute_total_area',
    )
    best_price = fields.Float(
        compute='_compute_best_price',
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offers.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offers.mapped('price'))

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None
