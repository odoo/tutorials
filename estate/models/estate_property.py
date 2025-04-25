import datetime

from odoo import api, fields, models
from odoo.excepetions import UserError, ValidationError
from odoo.tools import float_utils


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(string="Title")
    seller_id = fields.Many2one(
        "res.users", string="Salesperson", index=True, copy=True, default=lambda self: self.env.user
    )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=datetime.datetime.now() + datetime.timedelta(days=90),
        copy=False,
    )
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copyright=False, copy=False)
    bedrooms = fields.Integer(default=4)
    living_area = fields.Integer()
    garden_area = fields.Integer()
    total_area = fields.Integer(compute="_compute_total_area")
    facades = fields.Integer()
    has_garage = fields.Boolean()
    has_garden = fields.Boolean()
    active = fields.Boolean(default=True)
    garden_orientation = fields.Selection(
        selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")]
    )
    status = fields.Selection(
        selection=[("new", "New"), ("offer_receieved", "Offer Recieved"), ("sold", "Sold"), ("cancelled", "Cancelled")],
        readonly=True,
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property type")
    property_tag_ids = fields.Many2many("estate.property.tag", string="Property tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    best_offer_price = fields.Float(compute="_compute_best_offer_price")

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "The expected price of a property must be strictly positive.",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price > 0)",
            "The selling price of a property must be strictly positive.",
        ),
    ]

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer_price(self):
        for record in self:
            record.best_offer_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("has_garden")
    def _onchange_has_garden(self):
        for record in self:
            if record.has_garden:
                record.garden_orientation = "north"
                record.garden_area = 10
            else:
                record.garden_orientation = False
                record.garden_area = False

    @api.constrains("selling_price")
    def _check_price(self):
        for record in self:
            if float_utils.float_compare(record.selling_price, record.expected_price * 0.9) > 0:
                raise ValidationError("The selling price cannot be lower than 90%% of the expected price.")

    def action_mark_property_as_sold(self):
        if "cancelled" in self.mapped("status"):
            raise UserError("Cannot sell a property that was canceled.")

        for record in self:
            record.status = "sold"

    def action_mark_property_as_cancelled(self):
        if "sold" in self.mapped("status"):
            raise UserError("Cannot cancel a property that was sold.")

        self.status = "cancelled"
