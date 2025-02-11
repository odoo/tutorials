from datetime import  timedelta  # Import required libraries
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Recurring Plans"
    _order = "id desc"

    name = fields.Char("Name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date( "Availability Date", copy=False,
        default=lambda self: (fields.datetime.today() + timedelta(days=90)).strftime("%Y-%m-%d"),)
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", copy=False, readonly=True, default=0.0 )
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
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
        string="State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",  # Default state is 'New'
        required=True,  # Make this field required
        copy=False,  # Do not copy this field when duplicating a record
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    user_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    partner_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer("Total Area", compute="_compute_total_area")
    best_price = fields.Integer("Best Price", compute="_compute_best_price")

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0 )",
            "The expected_price must be strictly positive.",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >=0 )",
            "The selling_price must be positive.",
        ),
    ]

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for estateproperty in self:
            estateproperty.total_area = (
                estateproperty.garden_area + estateproperty.living_area
            )

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for offer in self:
            offer.best_price = max(offer.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_partner_id(self):
        if self.garden:  # When garden is set to True
            self.garden_area = 10  # Set garden_area to an integer value
            self.garden_orientation = "north"  # Set to lowercase value "north"
        else:
            self.garden_area = 0  # If no garden, reset the area
            self.garden_orientation = ""

    def action_property_cancel(self):
        if self.state != "sold":
            self.state = "cancelled"
        else:
            raise UserError("sold property can not be cancel.")

    def action_property_sold(self):
        if self.state != "cancelled":
            self.state = "sold"
        else:
            raise UserError("cancelled property can not be sold.")

    @api.ondelete(at_uninstall=False)
    def _check_delete_condition(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError(f"You cannot delete the property '{record.name}' because its state is '{record.state}'.")

