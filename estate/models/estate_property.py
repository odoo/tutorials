from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = 'Listing for the properties'

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='PostCode', index=True)
    date_availability=fields.Date(
        string='Available Date',
        default=lambda self: fields.Date.add(fields.Date.today(), months=3),
        copy=False
    )
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area(sqm)')
    facades = fields.Integer(
        string='Facades',
        help="a facade refers to the front or exterior appearance of a building, usually facing the street."
    )
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area(sqm)')
    garden_orientation = fields.Selection(
        string="Gardern Orientation",
        selection=[
            ('north','North'),
            ('south', 'South'),
            ('west', 'West'),
            ('east', 'East')
        ])
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection(
        string="Status",
        selection=[
            ('new','New'),
            ('offer_recevied','Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold','Sold'),
            ('cancelled','Cancelled')
        ],
        required=True,
        copy=False,
        default='new'
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    property_tag_ids = fields.Many2many("estate.property.tag", string="Property Tag")
    user_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    property_offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

    best_price = fields.Float(string="Best Offer", compute="_compute_best_price", store="True")

    @api.depends('property_offer_ids')
    def _compute_best_price(self):
        for record in self:
            if record.property_offer_ids:
                record.best_price = max(record.property_offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    total_area = fields.Integer(string="Total Area(sqm)", compute="_compute_total_area")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False
