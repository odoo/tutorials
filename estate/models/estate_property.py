from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char(required=True, tracking=True)
    description = fields.Text()
    postcode = fields.Char(tracking=True)
    date_availability = fields.Date()
    expected_price = fields.Float(required=True, tracking=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Garden Orientation",
        tracking=True,
    )
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
        string="Status",
    )
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesman_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user,
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_total_area", string="Total Area (sqm)")
    best_offer = fields.Float(compute="_compute_best_offer", string="Best Offer")

    _check_negative_expected_price = models.Constraint(
        "CHECK(expected_price >= 0)",
        "Expected value can't be negative, check your Math!",
    )
    _check_negative_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)",
        "Do you actually give money while selling your Property? Selling Price can't be negative, check your Math!",
    )

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped("price"), default=0)

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                if (float_compare(record.selling_price, (record.expected_price * 0.9), precision_digits=2) == -1):
                    raise ValidationError("The Selling Price cannot be less than 90% of Expected Price.")

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_new_cancelled(self):
        for record in self:
            if record.state not in ("new", "cancelled"):
                raise UserError("""Only properties which are "New" or "Cancelled" can be deleted!""")

    def action_sold(self):
        if self.state == "cancelled":
            raise UserError("Cancelled Property cannot be Sold")
        if self.state != "offer_accepted":
            raise UserError("You cannot sell the property if you haven't received an offer AND have an offer accepted!")
        self.state = "sold"
        return True

    def action_cancelled(self):
        if self.state == "sold":
            raise UserError("Sold Property cannot be Cancelled")
        self.state = "cancelled"
        return True
