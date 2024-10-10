from datetime import date, timedelta
from odoo import api, fields, models  # type: ignore

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Application Ayve"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: (date.today() + timedelta(days=90)).strftime('%Y-%m-%d'), copy=False)
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Integer(compute="_total_area", store=True)
    best_price=fields.Integer(compute="_compute_best_price", store=True)
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string='Garden Orientation',
        help='Select One Orientation'
    )
    active = fields.Boolean(default=True)
    
    state = fields.Selection(
    [
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ],
        string='State',
        default='new',
        copy=False,
        help='Select the current status of the property'
    )

    property_type_id=fields.Many2one("estate.property.type", string="Property Type")
    seller_id=fields.Many2one("res.users", string="Salesman" ,default=lambda self: self.env.user)
    buyer_id=fields.Many2one("res.partner", string="Buyer")
    tag_ids=fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids=fields.One2many("estate.property.offer", "property_id", string="Offers")

    @api.depends("living_area","garden_area")
    def _total_area(self):
        for line in self:
            line.total_area = line.living_area + line.garden_area

    @api.depends("best_price")
    def _compute_best_price(self):
        for record in self:
            record.best_price=100
        