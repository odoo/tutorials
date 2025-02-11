from odoo import fields, models, api
from datetime import date, timedelta
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate App"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=lambda self: date.today() + timedelta(days=90)
    )
    expected_price = fields.Float()
    selling_price = fields.Float(copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    is_garage = fields.Boolean(string="Garage")
    is_garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )
    status = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_reject", "Offer Rejected"),
            ("offer_accept", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        required=True,
        copy=False,
    )
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one("estate.property.type")
    salesman_id = fields.Many2one(
        "res.users",
        string="Salesman",
        ondelete="restrict",
        default=lambda self: self.env.user,
    )
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        ondelete="restrict",
        copy=False,
    )
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", inverse_name="property_id")
    total_area = fields.Integer(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer")

    _sql_constraints = [
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "Selling Price of the property should be positive",
        )
    ]

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            if not record.offer_ids:
                record.best_offer = 0
                continue
            record.best_offer = max(record.offer_ids.mapped("price"))

    @api.onchange("is_garden")
    def _onchange_is_garden(self):
        if self.is_garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_estate_property_sold(self):
        print("Sold button clicked")
        for record in self:
            if (
                record.status == "new"
                or record.status == "offer_accept"
                or record.status == "offer_reject"
            ):
                record.status = "sold"
            elif record.status == "cancelled":
                raise UserError("Cancelled property can't be sold")
            else:
                raise UserError("Property already sold")

        return True

    def action_estate_property_cancel(self):
        print("Cancel Button Clicked")
        for record in self:
            if (
                record.status == "new"
                or record.status == "offer_accept"
                or record.status == "offer_reject"
            ):
                record.status = "cancelled"
            elif record.status == "sold":
                raise UserError("Sold property can't be cancelled")
            else:
                raise UserError("Property already cancelled")

        return True

    @api.constrains(
        "expected_price",
    )
    def _check_expected_price(self):
        for record in self:
            if record.expected_price <= 0:
                raise ValidationError("Expected Price should be strictly positive")
