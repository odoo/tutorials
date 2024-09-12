from odoo import api, models, fields
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError


class estateproperty(models.Model):
    _name = "estate.property"
    _description = "estate module for different purpose"
    _order = "id desc"

    title = fields.Char("title", default="Unknown")
    myestate_model = fields.Text(string="description")
    Postcode = fields.Char("postcode")
    date_availability = fields.Date(
        "Available From", copy=False, default=datetime.now() + relativedelta(months=3)
    )
    expected_price = fields.Float(string="Expected Price", default=0)
    selling_price = fields.Float(
        string="Selling Price", copy=False, readonly=True, default=0
    )
    Bedrooms = fields.Integer("Bedrooms", default=3)
    living_area = fields.Integer("Living Area(sqm)", default=2)
    facades = fields.Integer("Facades", default=2)
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden_area", default=0)
    garden_orientation = fields.Selection(
        [("North", "North"), ("South", "South"), ("East", "East"), ("West", "West")]
    )
    active = fields.Boolean("Active", default=True)
    status = fields.Selection(
        [
            ("new", "New"),
            ("Offer Received", "Offer Received"),
            ("Offer Accepted", "Offer Accepted"),
            ("Sold", "Sold"),
            ("Cancelled", "Cancelled"),
        ],
        default="new",
        copy=False,
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.users", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total = fields.Float(compute="_compute_total", string="Total Area(sqm)")
    best_price = fields.Float(
        compute="_compute_max_price", string="Best offer", store=True
    )
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

    @api.depends("offer_ids.price")
    def _compute_max_price(self):
        for ele in self:
            ele.best_price = max(ele.mapped("offer_ids.price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 100
            self.garden_orientation = "North"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_sold(self):
        for record in self:
            if record.status == "Cancelled":
                raise UserError("Cancelled properties cannot be sold")
            else:
                record.status = "Sold"

    def action_cancel(self):
        for record in self:
            if record.status == "Sold":
                raise UserError("Sold properties cannot be cancelled")
            else:
                record.status = "Cancelled"

    @api.constrains("selling_price", "expected_price")
    def validate_selling_price(self):
        for record in self:

            if (
                record.selling_price < (0.9 * record.expected_price)
                and record.selling_price != 0
            ):
                raise ValidationError(
                    "the selling price cannot be lower than 90% of the expected price."
                )

    @api.ondelete(at_uninstall=False)
    def _prevent_property_deletion(self):
        for record in self:
            if record.status not in ("new", "Cancelled"):
                raise UserError("Only new and cancelled properties can be deleted")

    # def check_limit(self, vals):
    #     self.status == "Offer Received"
    #     if vals.get("price") <= self.best_price:
    #         raise ValidationError("the offer must be higher than best price")
