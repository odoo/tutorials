from datetime import  timedelta  # Import required libraries

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _inherit = ['mail.thread']
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char("Name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")  
    date_availability = fields.Date( "Availability Date", copy=False,
        default=lambda self: (fields.Datetime.today() + timedelta(days=90)).strftime("%Y-%m-%d"),)
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
    company_id = fields.Many2one("res.company", string="Company Id", default = lambda self:self.env.company, required=True)

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
        for estateproperty in self:
            estateproperty.best_price = max(estateproperty.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:  # When garden is set to True
            self.garden_area = 10  # Set garden_area to an integer value
            self.garden_orientation = "north"  # Set to lowercase value "north"
        else:
            self.garden_area = 0  # If no garden, reset the area
            self.garden_orientation = ""

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        if not float_is_zero(self.selling_price, precision_rounding=2) and float_compare(self.selling_price,
            self.expected_price * 0.9, precision_rounding=2) < 0:
                 raise UserError("Selling price must be at least 90% greater than expected price.")
                  

    def action_property_cancel(self):
        if self.state != "sold":
            self.state = "cancelled"
        else:
            raise UserError("sold property can not be cancel.")

    def action_property_sold(self):
        if not self.selling_price:
            raise UserError("without offer you can not sold property")
        elif self.state == "cancelled":
            raise UserError("cancelled property can not be sold.")
        else :
            self.state = "sold"
            self.message_post(
            body=f"Property '{self.name}' has been sold.",
            message_type='notification',
            subject="Property Sold",)

    @api.ondelete(at_uninstall=False)
    def _check_delete_condition(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError(f"You cannot delete the property '{record.name}' because its state is '{record.state}'.")
                