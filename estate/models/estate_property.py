from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"

    _description = "Estate Management Model"

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "Expected price must be strictly positive.",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "Selling price must be positive.",
        ),
    ]

    _order = "id desc"

    active = fields.Boolean(default=True)  # reserved field

    state = fields.Selection(
        [
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )

    name = fields.Char(required=True)

    description = fields.Text("Description")

    postcode = fields.Char("Postcode")

    date_availability = fields.Date(
        "Available From",
        copy=False,
        default=lambda self: fields.Date.today() + relativedelta(months=3),
    )

    expected_price = fields.Float("Expected Price", copy=False)

    selling_price = fields.Float("Selling Price", required=True, readonly=True, copy=False)

    property_type_id = fields.Many2one("estate.property.type", string="Property Type", required=True)

    bedrooms = fields.Integer("Bedrooms", default=2)

    living_area = fields.Integer("Living Area (sqm)", default=0)

    facades = fields.Integer("Fences")

    garage = fields.Boolean("Garage")

    garden = fields.Boolean("Garden")

    garden_area = fields.Integer("Garden Area (sqm)")

    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
    )

    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
        required=True,
    )

    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)

    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Integer("Total Area", compute="_compute_total_area", store=True)

    best_price = fields.Float("Best Offer Price", compute="_compute_best_price", store=True)

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for estate in self:
            estate.total_area = estate.living_area + estate.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for estate in self:
            estate.best_price = max(estate.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def on_change_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def sell(self):
        for estate in self:
            if estate.state == "cancelled":
                raise UserError(_("You can't sell a cancelled property."))
            else:
                estate.state = "sold"

        return True

    def cancel(self):
        for estate in self:
            if estate.state == "sold":
                raise UserError(_("You can't cancel a sold property."))
            else:
                estate.state = "cancelled"

        return True

    # @api.constrains("state", "selling_price", "expected_price")
    # def _check_selling_price(self):
    #     for estate in self:
    #         if (
    #             estate.state == "offer_accepted"
    #             and float_compare(
    #                 estate.selling_price, 0.9 * estate.expected_price, precision_digits=0
    #             )
    #             < 0
    #         ):
    #             raise models.ValidationError(
    #                 "Selling price must be at least 90% of the expected price when property is sold."
    #             )

    @api.ondelete(at_uninstall=False)
    def _unlink(self):
        for estate in self:
            if estate.state not in ("new", "cancelled"):
                raise models.UserError(_("You cannot delete a property that is not in 'New' or 'Cancelled' state."))
