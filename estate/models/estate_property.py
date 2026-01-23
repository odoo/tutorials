from dateutil.relativedelta import relativedelta
from odoo import models, fields, api


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate Property app like immoweb"

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    offer_ids = fields.One2many("estate.property.offer", string="Offers", inverse_name="property_id")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    salesman = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.uid)
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    date_availability = fields.Date(string="Available From", default=fields.Date.today() + relativedelta(months=3), copy=False)
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    active = fields.Boolean(string="Active", default=True)
    total_area = fields.Float(string="Total Area", compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West")
        ]
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
        default="new"
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price")) if record.offer_ids else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = None
        else:
            self.garden_area = 10
            self.garden_orientation = "north"
