from odoo import fields, models, api
from odoo.exceptions import UserError
from datetime import timedelta, datetime

class RealEstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property Table"
    _order = "id desc"

    # Basic property fields
    id = fields.Integer()  # Internal ID field (not needed explicitly as Odoo manages it)
    create_uid = fields.Integer()  # ID of the user who created the record
    create_date = fields.Datetime(
        "Create Date", readonly=True, default=fields.Datetime.now
    )  # Auto-filled creation timestamp
    write_uid = fields.Integer()  # ID of the last user who modified the record
    write_date = fields.Datetime(
        "Write Date", readonly=True, default=fields.Datetime.now
    )  # Auto-filled last modification timestamp

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

    # Computed field: Total area (Living Area + Garden Area)
    total_area = fields.Float(
        string="Total Area",
        compute="_compute_total_area",
        store=True  # Store the computed value in the database
    )

    # defined constraints
    _sql_constraints = [
        ("positive_expected_price", "CHECK(expected_price > 0)",
         "A property expected price must be positive."),

        ("positive_selling_price", "CHECK(selling_price > 0)",
         "A property selling price must be positive.")
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        """ Computes the total area of the property as the sum of living area and garden area. """
        for record in self:
            record.total_area = record.living_area + record.garden_area

    # Computed field: Best offer price
    best_price = fields.Float(
        compute="_compute_best_price",
        string="Best Offer"
    )

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        """ Computes the best (highest) price from all offers on the property. """
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    # Relationship with Property Type model
    property_type = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        required=True
    )

    # Relationship with Buyer (Partner model)
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False  # Buyer field should not be duplicated if the property is copied
    )

    # Salesperson: Defaults to the currently logged-in user
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user
    )

    # Many-to-Many relationship with property tags
    tags_ids = fields.Many2many("estate.property.tag", string="Property Tags")

    # One-to-Many relationship with offers
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers"
    )

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
            if record.state not in["new", "cancelled"]:
                raise UserError("You can only delete new or cancelled properties!")
