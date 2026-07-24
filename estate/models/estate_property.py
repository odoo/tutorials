from datetime import date, datetime, time
from dateutil.relativedelta import relativedelta

from odoo import api, _, exceptions, fields, models


class EstateProperty(models.Model):
    _name = "realestate.properties"
    _description = "Real estate properties"

    active = fields.Boolean(default=True)
    name = fields.Char("Plan Name", required=True, translate=True)
    description = fields.Text("Notes")
    postcode = fields.Char("Postcode", required=True)
    date_availability = fields.Date(
        "Availability date",
        copy=False,
        default=date.today() + relativedelta(months=3),
    )
    expected_price = fields.Float("Expected price", required=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        default="new",
        copy=False,
    )
    selling_price = fields.Float("Selling price", copy=False, readonly=True)
    bedrooms = fields.Integer("Bedrooms", default=2)
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    living_area = fields.Integer("Living area (sqm)")
    garden_area = fields.Integer("Garden area (sqm)")
    total_area = fields.Integer("Total area (sqm)", compute="_compute_total_area")
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    best_offer = fields.Float("Best Offer", compute="_compute_best_price")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    sale_rep_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    property_type_id = fields.Many2one("realestate.properties.type")
    property_tag_ids = fields.Many2many("realestate.properties.tag", string="Tags")
    offer_ids = fields.One2many(
        "realestate.properties.offer",
        "property_id",
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped("price"))

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def sold_action_btn(self):
        for record in self:
            if record.state == "cancelled":
                raise exceptions.UserError(_("Cancelled properties cannot be sold"))

            record.state = "sold"

    def cancelled_action_btn(self):
        for record in self:
            if record.state == "sold":
                raise exceptions.UserError(_("Sold properties cannot be cancelled"))
            record.state = "cancelled"
