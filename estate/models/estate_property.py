from datetime import date

from odoo import fields, models, api
from odoo.tools import date_utils
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "A property module that adds the property as a listing"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=lambda _: date_utils.add(date.today(), months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    total_area = fields.Float(compute="_compute_total_area")
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offer-received", "Offer Received"),
            ("offer-accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one("res.partner", copy=False)
    seller_id = fields.Many2one(
        "res.users", name="Salesperson", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offers_ids = fields.One2many(
        "estate.property.offer", "property_id", string="Offers"
    )
    best_price = fields.Float(
        compute="_compute_best_price", readonly=True, string="Best Offer"
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for single_property in self:
            single_property.total_area = (
                single_property.living_area + single_property.garden_area
            )

    @api.depends("offers_ids.price")
    def _compute_best_price(self):
        for single_property in self:
            if single_property.offers_ids:
                single_property.best_price = max(
                    single_property.offers_ids.mapped("price")
                )
            else:
                single_property.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_property_cancel(self):
        for single_property in self:
            if single_property.state == "sold":
                raise UserError("Sold properties cannot be cancelled!")
                return False
            single_property.state = "cancelled"
        return True

    def action_property_sold(self):
        for single_property in self:
            if single_property.state == "cancelled":
                raise UserError("Cancelled properties cannot be sold!")
                return False
            single_property.state = "sold"
        return True
