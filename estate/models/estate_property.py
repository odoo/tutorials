from dateutil.relativedelta import relativedelta

from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.tools import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Management Module"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char(string="Post Code")
    date_availability = fields.Date(
        string="Availability From",
        default=lambda self: fields.Date.today() + relativedelta(months=3),
        copy=False,
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bed Rooms", default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    state = fields.Selection(
        string="Status",
        default="new",
        copy=False,
        required=True,
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("accepted", "Accepted"),
            ("sold", "Sold"),
            ("canceled", "Cancelled"),
        ],
    )
    active = fields.Boolean(default=True)
    tag_ids = fields.Many2many(
        "estate.property.tag", relation="mahiv", string="Property Tag"
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesman_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer")
    _check_positive_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "Expected Price Must be in Positive",
    )
    _check_positive_selling_price = models.Constraint(
        "CHECK(selling_price > 0)",
        "Selling Price Must be in Positive",
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        max_price_list = self.env["estate.property.offer"]._read_group(
            domain=[("property_id", "in", self.ids)],
            aggregates=["price:max"],
            groupby=["property_id"],
        )
        price_list = {record.id: price for record, price in max_price_list}
        for record in self:
            if record.id:
                record.best_offer = price_list.get(record.id, 0.0)
            else:
                record.best_offer = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def onchange_garden(self):
        if self.garden:
            self.garden_area = 1000
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        if self.state != "canceled":
            self.state = "sold"
        else:
            raise UserError("You cannot move to canceled stage after sold the property")
        return True

    def action_cencel(self):
        if self.state != "sold":
            self.state = "canceled"
        else:
            raise UserError("You cannot move to sold stage after cenceled the property")
        return True

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for record in self:
            if record.expected_price:
                minimum_price = record.expected_price * 0.9

                if float_compare(record.selling_price, minimum_price, 4) <= 0:
                    raise UserError(
                        "Selling price cannot be lower than 90% of the expected price."
                    )
