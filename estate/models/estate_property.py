from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.tools.float_utils import float_compare, float_is_zero
from odoo.exceptions import UserError, ValidationError

class EstateProperty(models.Model):
    # Model Configuration
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"
    _inherit = ['mail.thread']

    #---------------------------------------------------------------------
    # SQL Constraints
    #---------------------------------------------------------------------
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be positive'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The expected price must be positive'),
    ]

    #---------------------------------------------------------------------
    # Fields
    #---------------------------------------------------------------------
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Integer(string="Postcode")
    date_availability = fields.Date(
        string="Availability Date",
        default=lambda self:fields.Datetime.today() + relativedelta(days=90),
    )
    image = fields.Binary(string="Image")
    expected_price = fields.Float(string="Expected Price", required=True, tracking=True)
    best_price = fields.Float(compute="_compute_best_offer", string="Best Offer")
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)", default=0)
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area")
    active = fields.Boolean(string="Active",default=True, tracking=True)
    status = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        default="new",
        copy=False,
        tracking=True
    )
    company_id = fields.Many2one("res.company", string="Company", required=True, default= lambda self: self.env.company)

    #---------------------------------------------------------------------
    # Relations
    #---------------------------------------------------------------------
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")

    # Salesmen
    user_id = fields.Many2one("res.users", string="Salesmen", copy=False, default = lambda self: self.env.user)
    # Buyer
    partner_id = fields.Many2one("res.partner", string="Buyer", readonly=True)

    tag_ids = fields.Many2many("estate.property.tag", string="Tag")

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offer")


    #---------------------------------------------------------------------
    # Compute Methods
    #---------------------------------------------------------------------
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area


    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price")) if record.offer_ids else 0.0


    # --------------------------- Onchange Methods ---------------------------    
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""


    # --------------------------- Action Methods ---------------------------
    def action_property_sold(self):
        if self.selling_price == 0:
            raise UserError("No any offer found")

        for record in self:
            if record.status == "sold":
                raise UserError("Property is already Sold")
            if record.status == "cancelled":
                raise UserError("Cancelled property cannot be Sold")
            else:
                record.status = "sold"

    def action_property_cancel(self):
        for record in self:
            if record.status == "sold":
                raise UserError("Sold property cannot be Cancelled")
            else:
                record.status = "cancelled"
                record.partner_id = ""

    # --------------------------- Ondelete Methods ---------------------------
    @api.ondelete(at_uninstall=False)
    def _unlink_property(self):
        for record in self:
            if record.status not in ('new', 'cancelled'):
                raise UserError("You cannot delete the property which status is not new or cancelled")
            

    #---------------------------------------------------------------------
    # Python Constraints
    #---------------------------------------------------------------------
    @api.constrains("selling_price")
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) == -1:
                    raise ValidationError("The selling price cannot be lower then 90% of the expected price")

