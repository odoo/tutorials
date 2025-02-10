from odoo import models, fields, api
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "public.property"
    _description = "Estate related data"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        "Available From",
        default=lambda self: (datetime.today() - relativedelta(month=3)).date(),
        copy=False,
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
        [("north", "North"), ("east", "East"), ("west", "West"), ("south", "South")]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            (
                "offer_received",
                "Offer Received",
            ),
            (
                "offer_accepted",
                "Offer Accepted",
            ),
            (
                "sold",
                "Sold",
            ),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        copy=False,
    )
    propertytype_id = fields.Many2one("public.property.type", string="Property type")
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson = fields.Many2one(
        "res.users", string="Sales Person", default=lambda self: self.env.user
    )
    tags_ids = fields.Many2many("public.property.tag", string="Tags")
    offer_ids = fields.One2many("public.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_total")
    best_price = fields.Float(compute="_compute_best_price")

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "The expected price must be positive.",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price > 0)",
            "The selling price must be positive.",
        ),
    ]

    rounding_precision = 0.0001

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for record in self:
            if record.expected_price == 0:
                break
            if (
                float_compare(
                    record.expected_price * 0.9,
                    record.selling_price,
                    precision_rounding=self.rounding_precision,
                )
                >= 0
            ):
                raise ValidationError(
                    "The selling price cannot be less than the 90% of expected price"
                )

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = self.living_area + self.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def sold(self):
        if self.state == "cancelled":
            raise UserError("A cancelled property cannot be sold")
        for record in self:
            record.state = "sold"

    def cancelled(self):
        if self.state == "sold":
            raise UserError("A sold property cannot be cancelled")
        for record in self:
            record.state = "cancelled"


class PropertyType(models.Model):
    _name = "public.property.type"
    _description = "A different types of properties."

    name = fields.Char()
    _sql_constraints = [
        ("uniq_property_type", "unique(name)", "A property type must be unique.")
    ]


class PropertyTag(models.Model):
    _name = "public.property.tag"
    _description = "Property Tags"

    name = fields.Char(required=True)
    _sql_constraints = [
        ("uniq_property_tag", "unique(name)", "A property tag must be unique.")
    ]


class PropertyOffer(models.Model):
    _name = "public.property.offer"
    _description = "Property Offers"
    _sql_constraints = [
        ("check_price", "CHECK(price >= 0)", "The offer price must be positive.")
    ]

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("public.property", required=True)

    validity = fields.Integer(string="Validity (Days)", default=7)
    date_deadline = fields.Date(
        string="Deadline Date",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(
                    days=record.validity
                )

            else:
                record.date_deadline = False

    @api.depends("date_deadline")
    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                deadline = record.date_deadline
                record.validity = (deadline - record.create_date.date()).days
            else:
                record.validity = 7

    def action_confirm(self):
        for record in self:
            record.status = "accepted"
            record.property_id.buyer = record.partner_id
            record.property_id.selling_price = record.price

    def action_cancle(self):
        for record in self:
            record.status = "refused"
