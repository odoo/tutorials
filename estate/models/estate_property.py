from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char("Title", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")

    def _default_Date(self):
        return datetime.now() + relativedelta(months=3)

    property_type_id = fields.Many2one("estate.property.type", "Type")
    date_availability = fields.Date("Available From", copy=False, default=_default_Date)
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float(
        "Selling Price",
        readonly=True,
        copy=False,
    )
    sales_man_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    property_tag = fields.Many2many("estate.property.tag", string="Tags")
    property_offer_id = fields.One2many("estate.property.offer", "property_id", "Offer")
    active = fields.Boolean(string="Active", default=True)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new",
    )
    total_area = fields.Float("Total Area", compute="_compute_total")
    best_price = fields.Float("Best Price", compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.depends("property_offer_id.price")
    def _compute_best_price(self):
        if self.property_offer_id:
            offer_price = self.property_offer_id.mapped("price")
            self.best_price = max(offer_price)
        else:
            self.best_price = 0.0
