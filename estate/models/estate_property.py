from datetime import timedelta
from odoo import api, exceptions, fields, models
from odoo.tools.float_utils import float_compare, float_is_zero
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class estateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, 
        default=lambda self: fields.Date.today() + timedelta(days=90)
    )  
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
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
    )
    active = fields.Boolean(default=True)
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
    )
    property_type_id = fields.Many2one(
        "estate.property.type", 
        string="Property Type"
    )
    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Property Tag"
    )
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    # Add the One2many field to store the related offers
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    # Computed field for total_area
    total_area = fields.Float(string="Total Area", compute="_compute_total_area", store=True)
    # Computed field for find a best offer price 
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price", store=True)

    #constraint
    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "The expected price must be strictly positive."),
        ("check_selling_price", "CHECK(selling_price >= 0)", "The selling price must be positive."),
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for property in self:
            if property.offer_ids:
                property.best_price = max(property.offer_ids.mapped("price"))
            else:
                property.best_price = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10  # Default value for garden area
            self.garden_orientation = "north"  # Default value for garden orientation
        else:
            self.garden_area = 0  # Clear the garden area
            self.garden_orientation = False  # Clear the garden orientation

    def cancel_property(self):
        for property in self:
            if property.state == "sold":
                raise UserError("A sold property cannot be cancelled.")
            property.state = "cancelled"
    
    def set_sold(self):
        for property in self:
            if property.state == "cancelled":
                raise UserError("A cancelled property cannot be set as sold.")
            property.state = "sold"

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            # Skip the check if selling_price is zero (e.g., no offer validated yet)
            if float_is_zero(record.selling_price, precision_rounding=0.01):
                continue
            # Ensure selling_price is at least 90% of expected_price
            min_acceptable_price = 0.9 * record.expected_price
            if float_compare(record.selling_price, min_acceptable_price, precision_rounding=0.01) < 0:
                raise ValidationError(
                    "The selling price cannot be less than 90% of the expected price."
                )   

    @api.ondelete(at_uninstall=False)
    def _check_delete_state(self):
        for record in self:
            if record.state not in ["New", "Cancelled"]:
                raise exceptions.UserError("You cannot delete a property unless its state is 'New' or 'Cancelled'.")                 