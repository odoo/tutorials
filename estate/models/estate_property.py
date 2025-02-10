from dateutil.relativedelta import relativedelta
from odoo import api, models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "This is the model for estate property"


    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="PostCode")
    date_availability = fields.Date(string="Available From", copy=False, default=lambda self:fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area(sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West")
        ])
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        required=True,
        default="new",
        copy=False
    )
    property_type_id = fields.Many2one(comodel_name="estate.property.type", string="Property Type")
    buyer_id = fields.Many2one(comodel_name="res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(comodel_name="res.users", string="Salesman", default=lambda self:self.env.user)
    tag_ids = fields.Many2many(comodel_name="estate.property.tag", string="Property Tag")
    offer_ids = fields.One2many(comodel_name="estate.property.offer", inverse_name="property_id")
    total_area =fields.Integer(string="Total Area", compute="_compute_total_area")
    best_price = fields.Float(string="Best Price", compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0
    
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None
