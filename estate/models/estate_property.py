from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.orm.utils import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Table for property test tutoriel"
    _order = "id desc"

    name = fields.Char("Title", required=True, default="Unknown")
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        "Available From",
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(required=True)
    _check_expected_price = models.Constraint(
        "CHECK(expected_price >= 0)",
        "The price should be strictly positive",
    )
    selling_price = fields.Float(readonly=True, copy=False)
    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)",
        "The price should be strictly positive",
    )
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    property_type_id = fields.Many2one("estate.property.type")
    salesperson_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", copy=False, readonly=True)
    tags_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute="_total_area", readonly=True)
    best_price = fields.Float(compute="_best_price", readonly=True, string="Best Offer")

    @api.ondelete(at_uninstall=False)
    def _ondelete(self):
        for record in self:
            if record.state in ("new", "cancelled"):
                raise ValueError(
                    self.env._(
                        "You cannot delete a entry with a 'New' or 'Canceled' status.",
                    ),
                )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
            return
        self.garden_orientation = self.garden_area = None

    @api.depends("offer_ids.price")
    def _best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    @api.depends("living_area", "garden_area")
    def _total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("selling_price", "expected_price")
    @api.constrains("selling_price")
    def _onchange_constrains_selling_price(self):
        for record in self:
            if (
                not float_is_zero(record.selling_price, 3)
                and float_compare(
                    record.expected_price * 0.90,
                    record.selling_price,
                    3,
                )
                > 0
            ):
                raise ValidationError(
                    self.env._(
                        "selling price should be at least 90 percent of the expected price",
                    ),
                )

    def cancel(self):
        if self.state == "sold":
            raise UserError(self.env._("A sold property cannot be cancelled"))
        self.state = "cancelled"

    def sold(self):
        if self.state == "cancelled":
            raise UserError(self.env._("A cancelled property cannot be sold"))
        self.state = "sold"
