from odoo.tools import float_compare, float_is_zero
from odoo import api, fields, models, exceptions


# Class of EstateProperty to define fields of database table
class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Properties"
    _order = "id desc"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode", required=True)
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price ", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area(sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="State",
        required=True,
        copy=False,
        default="new"
    )
    total_area = fields.Float(string="Total Area(sqm)", compute="_compute_total_area")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    user_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tags", string="Tags")
    offer_ids = fields.One2many(
        "estate.property.offer", "property_id", string="Offers"
    )  # One2Many field
    best_prices = fields.Float(string="Best Offer", compute="_compute_best_offer")

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "Expected Price must be positive",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price > 0)",
            "Selling Price must be positive",
        ),
    ]

    # Function of computing total area
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    # Fucntion of deciding best price among available prices
    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for property in self:
            if property.offer_ids:
                property.best_prices = max(
                    property.offer_ids.mapped("price"), default=0.0
                )
            else:
                property.best_prices = 0.0

    @api.onchange("garden")
    def onchange_check_garden_status(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    # Function to perform action when property Sold
    def action_to_sold_property(self):
        for record in self:
            if record.state == "cancelled":
                raise exceptions.UserError("A cancelled property can not be sold")
            record.state = "sold"
        return True

    # Function to perform action when property Canceled
    def action_to_cancel_property(self):
        for record in self:
            if record.state == "sold":
                raise exceptions.UserError("A sold property can not be cancelled")
            record.state = "cancelled"
        return True

    # constrain of selling price not fall more lower than 90% expected price
    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, 2) != 1:
                threshold = record.expected_price * 0.90
                if float_compare(threshold, record.selling_price, 2) == 1:
                    raise exceptions.ValidationError(
                        "The selling price must be at least 90% of the expected price!You must reduce the expected price if you want to accept this offer."
                    )

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        """Prevent deletion if property state is not 'New' or 'Cancelled'."""
        for record in self:
            if record.state not in ("new", "cancelled"):
                raise exceptions.UserError(
                    "You cannot delete a property unless it is in 'New' or 'Cancelled' state."
                )
