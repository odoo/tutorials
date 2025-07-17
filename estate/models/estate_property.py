from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
from datetime import date
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Model"

    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    postcode = fields.Text(string="Postcode")
    date_availability = fields.Date(
        string="Date Availability",
        copy=False,
        default=lambda self: date.today() + relativedelta(months=3),
    )
    expected_price = fields.Float(string="Expected Price")
    selling_price = fields.Integer(string="Selling Price")
    bedrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")

    garden_orientation = fields.Selection(
        string="Type",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )

    active = fields.Boolean(default=True, string="Active")

    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received "),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="State",
        default="new",
        copy=False,
    )

    # property will have Many to one relation with property type since many properties can belong to one property type

    property_type_id = fields.Many2one("estate.property.type", "Property Type")

    user_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        copy=False,
    )

    partner_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False,
    )

    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Integer(
        compute="_compute_total_property_area", string="Total Area"
    )

    best_price = fields.Integer(compute="_compute_best_price", string="Best Price")

    status = fields.Char(default="new", string="Status")

    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company,
        required=True,
    )

    _order = "id desc"

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "Expected price must be strictly positive",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "Selling price should be positive",
        ),
    ]

    @api.depends("garden_area", "living_area")
    def _compute_total_property_area(self):
        for area in self:
            area.total_area = area.garden_area + area.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            offers_list = record.mapped("offer_ids.price")
            if offers_list:
                record.best_price = max(offers_list)
            else:
                record.best_price = 0

    # on change of garden status , update gardern area and its orientation

    @api.onchange("garden")
    def _onchange_garden_status(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
            return
        self.garden_area = 0
        self.garden_orientation = ""

    # acts when property is sold
    # In case property is cancelled it cannot be sold
    def action_sell_property(self):
        # dictionary for the property status
        property_sell_status_dict = {"new": True, "sold": True, "cancelled": False}

        for record in self:
            if property_sell_status_dict[record.status]:
                record.status = "sold"
                record.state = "sold"
            else:
                raise UserError("Cancelled property cannot be sold.")

    # action in case of cancel property button
    #  If property is sold than Cannot be cancelled

    def action_cancel_property_selling(self):
        property_cancel_status_dict = {
            "new": True,
            "cancelled": True,
            "sold": False,
        }
        for record in self:
            if property_cancel_status_dict[record.status]:
                record.status = "cancelled"
            else:
                raise UserError("Sold  property cannot be cancelled.")

    # constrains for the selling price

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for data in self:
            # if call will come after selling price change than it will allow updated price to work
            if data.selling_price <= 0:
                return

            price_float_ratio = data.selling_price / data.expected_price
            ratio_diffrence = float_compare(price_float_ratio, 0.9, precision_digits=2)
            if ratio_diffrence == -1:
                data.selling_price = 0
                raise ValidationError(
                    "The selling price cannot be lower than 90% of the expected price"
                )

    # delete opration for the process

    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_new_or_cancelled(self):
        for data in self:
            if not bool(data.state == "new" or data.state == "cancelled"):
                raise UserError(
                    "Can't delete property which is not in new or cancelled state!"
                )
