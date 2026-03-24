from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char(string='Title', required=True, default='Unknown')
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postal Code')
    last_seen = fields.Datetime(
        string="Last Seen", default=fields.Datetime.now)
    date_availability = fields.Date(
        string='Available From', copy=False, default=fields.Date.today() + relativedelta(months=+3)
    )
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(
        string='Selling Price', readonly=True, copy=False)
    living_area = fields.Float(string='Living Area (sq m)')
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    facades = fields.Integer(string='Facades')
    has_garage = fields.Boolean(string="Has Garage ?")
    has_garden = fields.Boolean(string="Has Garden ?")
    garden_area = fields.Integer(string="Garden Area (sq m)")
    active = fields.Boolean(string="Is Active ?", default=True)
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
    )
    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        required=True, default="new", copy=False
    )
    property_type_id = fields.Many2one(
        "estate.property.type", ondelete='Cascade', string="Property Type"
    )
    salesperson_id = fields.Many2one(
        "res.users", string="Sales Person", default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    property_tags_ids = fields.Many2many(
        "estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_area")
    best_price = fields.Float(
        string="Best Offer", compute="_compute_best_price"
    )

    @api.depends("living_area", "garden_area")
    def _compute_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for rec in self:
            if rec.offer_ids:
                rec.best_price = max(rec.offer_ids.mapped("price"))
            else:
                rec.best_price = 0.0
