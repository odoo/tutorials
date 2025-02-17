from odoo import api, fields, models
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Declare property for Real estate"
    _sql_constraints = [
        (
            "check_estate_property_selling_price",
            "CHECK(selling_price >= 0.0)",
            "Selling Price must be a positive amount",
        ),
        (
            "check_estate_property_expected_price",
            "CHECK(expected_price > 0.0)",
            "Expected Price must be a strictly positive amount",
        ),
        (
            "check_estate_property_bedrooms",
            "check(bedrooms > 0)",
            "Expected Bedrooms must be a strictly positive Number",
        ),
    ]
    # --------------------------------------- Fields Declaration ----------------------------------
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date("Available From", default=datetime.now() + timedelta(90))
    sequence = fields.Integer(default="1", help="Used to order records. Lower is better.")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default="2")
    living_area = fields.Integer()
    facades = fields.Integer()
    is_garage = fields.Boolean("Garage")
    is_garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (yard)")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="Choose the orientation of a garden from the options: North, South, East, or West.",
    )
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new",
    )
    active = fields.Boolean("Active", default=True)
    # Relational
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    user_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", readonly=True, copy=False)
    # Relational Field for tag's (Many2Many)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    # Relation Field for offer (one2Many)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_total_area")
    best_price = fields.Float(
        string="Best Offer", compute="_compute_best_price", help="Best offer so far."
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for value in self:
            if value.offer_ids:
                value.best_price = max(value.mapped("offer_ids.price"))
            else:
                value.best_price = 0.00

    @api.onchange("is_garden")
    def _onchange_garden(self): 
        if self.is_garden:
            self.garden_area = 20
            self.garden_orientation = "south"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _check_before_delete(self):
        for record in self:
            if record.state not in ["new", "cancelled"]:
                raise UserError(
                    f"You cannot delete a property because it is in {record.state} state."
                )

    @api.constrains("expected_price", "selling_price")
    def _check_price_difference(self):
        for prop in self:
            if prop.selling_price and prop.selling_price < prop.expected_price * 0.90:
                raise ValidationError(
                    "The selling price must be at least 90% of the expected price! You must reduce the expected price if you want to accept this offer."
                )
    # ---------------------------------------- Action Methods -------------------------------------
    def action_sold(self):
        if self.state == "cancelled":
            raise UserError("Cancelled properties cannot be sold.")
        if self.state == "sold":
            raise UserError("This property are already Sold!!")
        self.write({"state": "sold"})

    def action_cancel(self):
        if self.state == "sold":
            raise UserError("Sold properties cannot be cancelled.")
        self.write({"state": "cancelled"})
