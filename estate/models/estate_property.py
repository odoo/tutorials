from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.orm.decorators import ondelete
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "An estate property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda _model: fields.Date.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
    )
    total_area = fields.Integer(
        string="Total Area (sqm)",
        compute="_compute_total_area",
    )
    state = fields.Selection(
        copy=False,
        selection=[
            ("new", "New"),
            ("received", "Offer Received"),
            ("accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        required=True,
    )
    active = fields.Boolean(default=True)

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    seller_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user,
    )

    property_tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    best_price = fields.Float(compute="_compute_best_price")

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "A property expected price must be strictly positive.",
    )
    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)",
        "A property selling price must be positive.",
    )

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            offer_prices = record.offer_ids.mapped("price")
            record.best_price = max(offer_prices, default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_mark_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError(self.env._("Cancelled properties cannot be sold."))
            record.state = "sold"
        return True

    def action_mark_cancelled(self):
        for record in self:
            if record.state == "sold":
                raise UserError(self.env._("Sold properties cannot be cancelled."))
            record.state = "cancelled"
        return True

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price_high_enough(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            if (
                float_compare(
                    record.selling_price,
                    0.9 * record.expected_price,
                    precision_digits=2,
                )
                == -1
            ):
                raise ValidationError(
                    self.env._(
                        "The selling price must be at least 90% of the expected price! "
                        "You must reduce the expected price if you want to accept this offer.",
                    ),
                )

    @ondelete(at_uninstall=False)
    def _unlink_if_property_new_or_cancelled(self):
        if any(record.state not in ["new", "cancelled"] for record in self):
            raise UserError(
                self.env._("Only new and cancelled properties can be deleted."),
            )
