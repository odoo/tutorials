from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer received"),
            ("offer_accepted", "Offer accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        copy=False,
    )
    name = fields.Char(
        required=True,
        string="Title",
    )
    description = fields.Text(
        string="Description",
    )
    postcode = fields.Char(
        string="Postcode",
    )
    date_availability = fields.Date(
        default=fields.Date.add(fields.Date.today(), months=3),
        copy=False,
        string="Available from",
    )

    expected_price = fields.Monetary(
        string="Expected price", currency_field="currency_id",
    )

    selling_price = fields.Monetary(
        string="Selling price",
        readonly=True,
        copy=False,
        default_export_compatible=False,
        currency_field="currency_id",
    )
    currency_id = fields.Many2one(
        "res.currency", default=lambda self: self.env.company.currency_id,
    )

    bedrooms = fields.Integer(default=2, string="Bedrooms")
    living_area = fields.Integer(string="Living Area", default=0)
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    has_garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area", default=0)
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="If you don't know where West is, wait for the sun to go to sleep. Its bedroom lies West.",
    )

    customer_id = fields.Many2one("res.partner", string="Customer", copy=False)

    salesman_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user,
        required=True,
    )
    estate_property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
    )

    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="estate_property_id",
    )

    best_price = fields.Monetary(
        string="Best Offer",
        compute="_compute_best_price",
    )

    #### CONSTRAINTS ####
    _check_expected_price_positive = models.Constraint(
        "CHECK(expected_price > 0)",
        "Expected price must be positive",
    )

    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)",
        "the selling price must be positive.",
    )

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for ep in self:
            if float_is_zero(ep.selling_price, precision_digits=2):
                continue

            lowest_selling_price = ep.expected_price * 0.9
            if float_compare(ep.selling_price, lowest_selling_price, precision_digits=2) == -1:
                raise ValidationError(
                    _(
                        "The selling price must be at least 90%% of the expected price! "
                        "(Minimum expected: %s)", lowest_selling_price,
                    ),
                )

    #### COMPUTED VALUES ####
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for ep in self:
            ep.total_area = (
                ep.living_area + ep.garden_area if ep.has_garden else ep.living_area
            )

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for ep in self:
            ep.best_price = max(ep.offer_ids.mapped("price")) if ep.offer_ids else None

    @api.onchange("has_garden")
    def _onchange_has_garden(self):
        if self.has_garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    #### CRUD ####

    #### ACTIONS ####
    def action_set_accepted(self):
        for ep in self:
            # removed validation this looks a bit empty...
            ep.state = "offer_accepted"

    def action_set_sold(self):
        for ep in self:
            if ep.state == "cancelled":
                raise UserError(_("Cancelled properties cannot be sold."))
            if ep.state == "sold":
                raise UserError(_("Sold properties cannot be sold (anymore)."))

            accepted_offer = ep.offer_ids.filtered(lambda o: o.status == "accepted")
            if not accepted_offer:
                raise UserError(_("You must accept an offer before selling the property."))

            ep.write({
                    "state": "sold",
                    "customer_id": accepted_offer[0].partner_id.id,
                    "selling_price": accepted_offer[0].price,
            })
        return True

    def action_set_cancelled(self):
        # todo: split action and validation (validation goes into python constraint)
        for ep in self:
            # todo later : add warning - dont know how to do this from the model
            if ep.state == "sold":
                raise UserError(_("A cancelled property cannot be sold"))
            ep.state = "cancelled"
        return True
