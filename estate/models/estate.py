from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class Estate(models.Model):
    _name = "estate_property"
    _description = "Real Estate"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Available From",
        default=fields.Date.today() + relativedelta(months=3),
        copy=False,
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("east", "East"),
            ("west", "West"),
            ("south", "South"),
        ],
    )
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    type_id = fields.Many2one(
        string="Property Type",
        comodel_name="estate_property_type",
    )
    salesman_id = fields.Many2one(
        string="Salesman",
        comodel_name="res.users",
        default=lambda self: self.env.user,
    )
    buyer_id = fields.Many2one(string="Buyer", comodel_name="res.partner", copy=False)
    tag_ids = fields.Many2many(string="Tags", comodel_name="estate_property_tag")
    offer_ids = fields.One2many(
        string="Offers",
        comodel_name="estate_property_offer",
        inverse_name="property_id",
    )
    total_area = fields.Float(string="Total Area", compute="_compute_total_area")
    best_offer = fields.Float(string="Best Offer", compute="_compute_best_offer")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        self.best_offer = (
            max(self.offer_ids.mapped("price")) if len(self.offer_ids) else 0.0
        )

    @api.onchange("garden")
    def _on_change_garden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = "north" if self.garden else None

    def action_sell_property(self):
        for property in self:
            if property.state == "cancelled":
                raise UserError("Cancelled properties cannot be sold")
            property.state = "sold"

        return True

    def action_cancel_property(self):
        for property in self:
            if property.state == "sold":
                raise UserError("Sold properties cannot be cancelled")
            property.state = "cancelled"

        return True
