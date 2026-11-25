from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    def calculate_date(self):
        return fields.Date.today() + relativedelta(months=3)

    name = fields.Char(required=True)
    description = fields.Text()
    date_availability = fields.Date(default=calculate_date)
    postcode = fields.Char(required=True)
    expected_price = fields.Float(required=True, default=False)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    selling_price = fields.Float(copy=False, readonly=True, default=0.0)

    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        copy=False,
    )
    active = fields.Boolean(default=True)

    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Cancelled"),
        ],
        copy=False,
        string="Status",
        default="new",
    )

    buyer_id = fields.Many2one("res.partner", copy=False)

    salesperson_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    property_tag_ids = fields.Many2many(
        "estate.property.tag",
        column1="estate_property_id",
        column2="estate_property_tag_id",
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers",
    )

    maintenance_ids = fields.One2many(
        "estate.property.maintenance",
        "property_id",
        string="Maintenance",
    )

    total_area = fields.Integer(string="Total Area", compute="_compute_total_area")

    best_price = fields.Float(
        string="Best Offer", compute="_compute_best_price", store=True
    )

    _check_unique_name = models.Constraint(
        "unique(name, postcode)", "Property Name should be Unique"
    )

    _check_positive = models.Constraint(
        "CHECK(expected_price > 0 AND selling_price >= 0)",
        "The Value Should be positive",
    )

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                if (
                    float_compare(
                        record.selling_price,
                        record.expected_price * 0.9,
                        precision_digits=2,
                    )
                    < 0
                ):
                    raise ValidationError(
                        self.env._(
                            "The selling price must be at least 90% of the expected price."
                        )
                    )

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = "north"
            else:
                record.garden_area = 0
                record.garden_orientation = False

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.ondelete(at_uninstall=False)
    def _unlink_property(self):
        for record in self:
            if record.state not in {"new", "canceled"}:
                raise UserError(
                    self.env._("Only new and canceled properties can be deleted.")
                )

    def action_sold(self):
        for record in self:
            if record.state == "new":
                raise UserError(
                    self.env._(f"This Property:  {record.name} do not have any offer.")
                )
            if record.state == "canceled":
                raise UserError(
                    self.env._(
                        f"A cancelled property: {record.name} cannot be set as sold."
                    )
                )
            if record.state == "offer_accepted":
                record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError(self.env._("A sold property cannot be cancelled."))
            record.state = "canceled"
        return True
