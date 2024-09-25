from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class estateproperty(models.Model):
    _name = "estate.property"
    _description = "estate_model"
    _order = "id desc"
    name = fields.Char("Title", default="Unknown")
    myestate_model = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        "Available From", copy=False, default=datetime.now() + relativedelta(months=3)
    )
    expected_price = fields.Float("Expected Price", default=0)
    selling_price = fields.Float("Selling Price", copy=False)
    bedrooms = fields.Integer("Bedrooms", default=3)
    living_area = fields.Integer("Living Area (sqm)", default=2)
    facades = fields.Integer("Facades", default=2)
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)", default=0)
    garden_orientation = fields.Selection(
        [("north", "north"), ("south", "south"), ("east", "east"), ("west", "west")]
    )
    active = fields.Boolean("Active", default=True)
    status = fields.Selection(
        [
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        copy=False,
    )
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    property_type = fields.Many2one("estate.property.type", string="Property Type")
    sale_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    Buyer_id = fields.Many2one("res.users", string="Buyer", copy=False)
    property_tag = fields.Many2many("estate.property.tag", string="Property Tag")
    offer_id = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total = fields.Float(compute="_compute_total", string="Total Area (sqm)")
    best_price = fields.Float(compute="_compute_price", string="Best offer")
    _sql_constraints = [
        (
            "check_sellingprice_expectedprice_not_negative",
            "CHECK(selling_price >= 0.0 and expected_price >= 0.0)",
            "The selling price and expected_price should be greater than 0.",
        ),
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for ele in self:
            ele.total = ele.living_area + ele.garden_area

    @api.depends("offer_id.price")
    def _compute_price(self):
        for ele in self:
            ele.best_price = max(ele.mapped("offer_id.price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 100
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def sold_button(self):
        if self.status == "cancelled":
            raise UserError("Cancelled Properties cannot be sold")
        else:
            self.status = "sold"

    def cancel_button(self):
        if self.status == "sold":
            raise UserError("sold Properties cannot be cancelled")
        else:
            self.status = "cancelled"

    @api.constrains("selling_price", "expected_price")
    def validate_selling_price(self):
        for record in self:
            if (
                record.selling_price < (0.9 * record.expected_price)
                and record.selling_price != 0.0
            ):
                raise ValidationError(
                    "the selling price cannot be lower than 90% of the expected price."
                )

    @api.ondelete(at_uninstall=False)
    def _prevent_property_deletion(self):
        for record in self:
            if record.status not in ("new", "Cancelled"):
                raise UserError("Only new and cancelled properties can be deleted")
