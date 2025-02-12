from odoo import fields, models, api
from odoo.tools import float_is_zero, float_compare
from odoo.exceptions import UserError
from datetime import timedelta, datetime

class RealEstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property Table"
    _order = "id desc"

    name = fields.Char(required=True)  # Property name
    description = fields.Text()  # Property description
    postcode = fields.Char("Postcode")  # Postal code of the property
    # Availability date: default is 90 days from creation
    date_availability = fields.Date(
        "Date Availability",
        default=lambda self: datetime.now().date() + timedelta(days=90),
        readonly=True, copy=False
    )
    # Price-related fields
    expected_price = fields.Float("Expected Price", required=True)  # The price the seller expects
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)  # Final sold price (if sold)
    # Property characteristics
    bedrooms = fields.Integer("Bedrooms", default=2)  # Default: 2 bedrooms
    living_area = fields.Integer("Living Area")  # Main living area in square meters
    facades = fields.Integer("Facades")  # Number of facades (external walls)
    garage = fields.Boolean("Garage")  # Does the property have a garage?
    garden = fields.Boolean("Garden")  # Does the property have a garden?
    garden_area = fields.Integer("Garden Area")  # Garden size in square meters
    # Garden orientation selection
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West")
        ],
        string="Garden Orientation"
    )
    # Property state
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        default="new",
        required=True
    )
    total_area = fields.Float(
        string="Total Area",
        compute="_compute_total_area",
        store=True  # Store the computed value in the database
    )
    best_price = fields.Float(
        compute="_compute_best_price",
        string="Best Offer"
    )
    property_type = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        required=True
    )
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False  # Buyer field should not be duplicated if the property is copied
    )
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user
    )
    # Many-to-Many relationship with property tags
    tags_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers"
    )
    # defined constraints
    _sql_constraints = [
        ("positive_expected_price", "CHECK(expected_price > 0)",
         "A property expected price must be positive."),

        ("positive_selling_price", "CHECK(selling_price > 0)",
         "A property selling price must be positive.")
    ]

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            # Set default values when garden is set to True
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    active = fields.Boolean("Active", default=True)  # Active status of the property

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        """ Computes the total area of the property as the sum of living area and garden area. """
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        """ Computes the best (highest) price from all offers on the property. """
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    def action_cancel(self):
        """Cancel a property. A Sold property cannot be cancelled."""
        for record in self:
            if record.state == "sold":
                raise UserError("A sold property cannot be cancelled!")
            record.state = "cancelled"

    def action_sold(self):
        """Mark a property as Sold. A cancelled property cannot be sold."""
        for record in self:
            if record.state == "cancelled":
                raise UserError("A cancelled property cannot be sold!")
            if not record.buyer_id:
                raise UserError("A buyer must be set before marking as sold!")
            if record.selling_price <= 0:
                raise UserError("Selling price must be set before marking as sold!")
            record.state = "sold"

    @api.ondelete(at_uninstall=False)
    def _prevent_delete(self):
        """ Prevent deletion of properties if no in 'new' or 'cancelled' state. """
        for record in self:
            if record.state not in {"new", "cancelled"}:
                raise UserError("You can only delete new or cancelled properties!")

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        """Ensures that the selling price is at least 90% of the expected price unless it is zero."""
        for record in self:
            if record.selling_price and record.expected_price:
                if not float_is_zero(record.selling_price, precision_digits=2):
                    min_price = record.expected_price * 0.9
                    if float_compare(record.selling_price, min_price, precision_digits=2) == -1:
                        raise models.ValidationError(
                            "The selling price cannot be lower than 90% of the expected price!"
                        )

