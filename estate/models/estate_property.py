from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Propety"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available Date",
        default=lambda self: (fields.Date.today() + relativedelta(months=3)),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        default="north",
    )
    active = fields.Boolean()
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        default="new",
        copy=False,
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
        string="Offers",
    )

    total_area = fields.Float(string="Total Area", compute="_compute_total_area")

    best_offer = fields.Float(
        string="Best Offer",
        compute="_compute_best_offer",
        store=True,
    )

    _sql_constraints = [
        (
            "check_expected_price_field",
            "CHECK(expected_price > 0)",
            "Expected price must be positive!",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "Selling price must be positive!",
        ),
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + (property.garden_area or 0)

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for property in self:
            best_offer = max(property.offer_ids.mapped("price"), default=0)
            property.best_offer = best_offer

    @api.onchange("garden")
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = False
        else:
            self.garden_area = 10
            self.garden_orientation = "north"

    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("A cancelled property cannot be set as sold")
            record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("A a sold property cannot be cancelled.")
            record.state = "cancelled"
        return True

    @api.ondelete(at_uninstall=False)
    def _unlink_check(self):
        for record in self:
            if record.state not in ["new", "cancelled"]:
                raise UserError("You can delete only a new or cancelled property.")
        return True
