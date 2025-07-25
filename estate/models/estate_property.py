from odoo import models, fields, api, exceptions
from odoo.tools import float_utils


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    _order = "id desc"

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price >0)",
            "The expected price should be stricly positive",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >0)",
            "The selling price should be stricly positive",
        ),
    ]

    name = fields.Char(required=True)
    active = True
    description = fields.Text()
    postcode = fields.Char()
    date_availibility = fields.Date(
        copy=False, default=fields.Date.add(fields.Date.today(), months=3)
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
            ("east", "East"),
            ("south", "South"),
            ("west", "West"),
        ],
        help="Orientation of the garden",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        copy=False,
        required=True,
    )

    property_type_id = fields.Many2one("estate.property.type", string="Property type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )

    tags_ids = fields.Many2many("estate.property.tag", string="Tags")

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offer")

    total_area = fields.Float(compute="_compute_total")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("garden_area", "living_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            maxi = 0
            for line in record.offer_ids:
                maxi = line.price if line.price > maxi else maxi
            record.best_price = maxi

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if (
                len(record.offer_ids) != 0
                and float_utils.float_compare(
                    record.selling_price,
                    0.9 * record.expected_price,
                    precision_digits=5,
                )
                == -1
            ):
                raise exceptions.ValidationError(
                    r"The selling price cannot be lower than 90% of the expected price"
                )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = ""
            self.garden_orientation = ""

    @api.ondelete(at_uninstall=False)
    def prevent_delete(self):
        for record in self:
            if (
                record.state == "offer_received"
                or record.state == "offer_accepted"
                or record.state == "sold"
            ):
                raise exceptions.AccessError(
                    "You can't delete a property if it's not New or Cancelled"
                )

    def sell_property(self):
        for record in self:
            if record.state != "cancelled":
                record.state = "sold"
            else:
                raise exceptions.UserError("A cancelled property can not be sold")

    def cancel_property(self):
        for record in self:
            if record.state != "sold":
                record.state = "cancelled"
            else:
                raise exceptions.UserError("A sold property can not be cancelled")
