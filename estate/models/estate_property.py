from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char(string='Title', required=True, default='Unknown')
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postal Code')
    date_availability = fields.Date(
        string='Available From', copy=False, default=fields.Date.today() + relativedelta(months=+3)
    )
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(
        string='Selling Price', readonly=True, copy=False
    )
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
        "estate.property.tag", string="Property Tags"
    )
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(
        string="Best Offer", compute="_compute_best_price"
    )

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)', 'Price must be strictly positive'
    )
    _check_selling_price = models.Constraint(
        'CHECK (selling_price > 0)', "Selling price must be strictly positive"
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        if self.offer_ids:
            self.best_price = max(self.offer_ids.mapped("price"))
        else:
            self.best_price = 0.0

    @api.onchange('has_garden')
    def _onchange_garden(self):
        if self.has_garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    def action_property_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled property cannot be set as sold.")
            else:
                record.state = "sold"
        return True

    def action_property_cancelled(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold property cannot be set as cancelled")
            else:
                record.state = "cancelled"
        return True
