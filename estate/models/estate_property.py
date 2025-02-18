from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "A new property is listed"
    _inherit = ["mail.thread", "mail.activity.mixin"]  # enables the chatter
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=fields.Datetime.today() + relativedelta(months=3)
    )
    expected_price = fields.Float(required=True, string="Expected Price:")
    selling_price = fields.Integer(readonly=True, copy=False, string="Selling Price:")
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Type",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        string="state",
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
        tracking=True,
    )
    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one(
        "res.partner", string="buyer_id", copy=False, tracking=True
    )
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", tracking=True)
    total_area = fields.Float(compute="_compute_area")
    best_price = fields.Float(compute="_compute_best_offer", tracking=True)
    seller_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user,
        tracking=True,
    )

    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company.id,
    )
    property_image = fields.Image("Property Image", max_width=1024, max_height=1024)
    _sql_constraints = [
        (
            "positive_expected_price",
            "CHECK(expected_price > 0)",
            "Expected price cannot be negative.",
        ),
        (
            "positive_selling_price",
            "CHECK(selling_price > 0)",
            "Selling_price cannot be negative.",
        ),
        ("unique_property_name", "UNIQUE(name)", "Property name should be unique"),
    ]

    @api.depends("living_area", "garden_area")
    def _compute_area(self):
        for area in self:
            if area:
                area.total_area = area.garden_area + area.living_area
            else:
                area.total_area = 0

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for offer in self:
            if offer.offer_ids:
                offer.best_price = max(offer.offer_ids.mapped("price"))
            else:
                offer.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None

    def sold(self):
        if self.state != "cancelled" and self.state == "offer accepted":
            self.state = "sold"
            print("Property Sold")
        else:
            print(
                "Property cannot be sold because it has either been cancelled or no offers have been accepted! ERROR RAISED"
            )
            raise UserError(
                "Property cannot be sold because it has either been cancelled or no offers have been accepted!"
            )

    def cancel(self):
        if self.state != "sold":
            self.state = "cancelled"
        else:
            raise UserError("Sold Property cannot be cancelled!")

    def action_offer(self):
        print("function called!")
        pass

    def unlink(self):
        for property in self:
            if property.state not in ["new", "cancelled"]:
                raise ValidationError("Only new and cancelled property can be deleted")

        # Call the super method to actually delete the property
        return super(EstateProperty, self).unlink()

    def _track_subtype(self, init_values):
        self.ensure_one()
        if "state" in init_values and self.state == "sold":
            return self.env.ref("estate.mt_state_change")
        return super()._track_subtype(init_values)
