from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class TestModel(models.Model):
    today = datetime.now()

    month = today.month + 3
    year = today.year
    day = today.day

    if month > 12:
        year = year + 1
        month = month % 12

    three_month_date = today.replace(year=year, month=month, day=day)

    _name = "estate.property"
    _description = "This is a dummy table"

    name = fields.Char(translate=True, default="Unknown", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=three_month_date.date())
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer()
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
        ],
        string="Direction",
        default="north",
    )
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Receeived"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ]
    )
    active = fields.Boolean("Active", default=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property_type")
    property_tag_ids = fields.Many2many(
        "estate.property.tag",
        relation="losbo_property_propertyTag",
        string="Property_Tag",
        ondelete="cascade",
    )

    buyer = fields.Many2one("res.partner", string="buyer", copy=False)
    user_id = fields.Many2one(
        "res.users", string="salesperson", default=lambda self: self.env.user
    )
    offer_ids = fields.One2many("estate.property.offers", "property_id")

    total_offers = fields.Integer(compute="_compute_offers")

    total_area = fields.Float(compute="_compute_area")
    best_price = fields.Integer(compute="_compute_price")

    @api.depends("offer_ids")
    def _compute_offers(self):
        for record in self:
            count = 0
            if record.offer_ids:
                for offers in record.offer_ids:
                    if offers.status == "accepted":
                        count += 1
            record.total_offers = count

    @api.constrains("name", "description")
    def _check_description(self):
        for record in self:
            if record.name == record.description:
                raise ValidationError("Fields name and description should not be equal")

    @api.depends("living_area", "garden_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_price(self):
        best_price = 0
        for records in self:
            for offers in records.offer_ids:
                best_price = max(offers.price, best_price)
            records.best_price = best_price
