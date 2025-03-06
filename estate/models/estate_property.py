from odoo import api,fields, models  # type: ignore
from datetime import date, timedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Description"

    # Database fields for PostgreSQL
    name = fields.Char(required=True,string="Title")
    description = fields.Text(string="Description of Property")
    postcode = fields.Char(string="Postcode")
    available_from = fields.Date(
        default=lambda self: date.today() + timedelta(days=90),
        string="Available From",
        copy=False
    )
    expected_price = fields.Float(string="Expected Price")
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    total_area = fields.Float(string="Total Area", compute="_compute_total_area", store=True)
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string="Garden Orientation",
        default="east",
    )
    status = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        string="Status",
        required=True,
        default="new",
        copy=False
    )
    active = fields.Boolean(string="Active", default=True)

    # Many2one Fields
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        required=True,
    )
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer"
    )
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user
    )

    # Many2many fields
    tag_ids = fields.Many2many(
       "estate.property.tag",
       string="Property Tags"
    )

    #One2many fields
    offer_ids = fields.One2many(
        "estate.property.offer", "property_id",
        string="Offers"
    )
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price", store=True)

    # Compute Total Area
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    # Compute
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

