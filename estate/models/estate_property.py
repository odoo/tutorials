from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"
    
    _sql_constraints = [
        (
            'positive_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be strictly positive'
        ),
    ]

    name = fields.Char(
        string="Property Name",
        required=True,
        help="Property Name"
    )
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        "Availability Date",
        copy=False,
        default=lambda self: fields.Date.today() + relativedelta(days=90),
    )
    expected_price = fields.Float("Expected Price", required=True, help="Expected Price")
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West")
        ],
        string="Garden Orientation",
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
        string="State",
        required=True,
        copy=False,
        default="new",
    )
    property_type_id=fields.Many2one(string="Property Type", comodel_name="estate.property.type", ondelete="restrict")
    buyer_id=fields.Many2one(string="Buyer", comodel_name="res.partner", copy=False, readonly=True)
    salesperson_id=fields.Many2one(
        string="Salesperson",
        comodel_name="res.users",
        default=lambda self: self.env.user,
        ondelete="restrict",
    )
    tag_ids=fields.Many2many(string="Tags", comodel_name="estate.property.tag", ondelete="restrict")
    offer_ids=fields.One2many(string="Offers", comodel_name="estate.property.offer", inverse_name="property_id")
    total_area=fields.Integer(compute="_compute_total_area")
    best_price=fields.Integer(compute="_compute_best_price", help="Best price from offers")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)
    
    @api.constrains("selling_price", "expected_price")
    def _check_valid_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2) and float_compare(record.selling_price, record.expected_price*0.9, precision_digits=2) < 0:
                raise ValidationError("Selling price must be atleast 90% of the expected price")
    
    @api.onchange("garden")
    def _onchange_garden_availability(self):
        if self.garden:
            self.garden_area=10
            self.garden_orientation="north"
        else:
            self.garden_area=0
            self.garden_orientation=""
        
    @api.ondelete(at_uninstall=False)
    def _check_property_before_unlink(self):
        for record in self:
            if record.state != 'new' and record.state != 'cancelled':
                raise UserError("Can only delete new or cancelled properties")
    
    def action_mark_property_sold(self):
        for record in self:
            if record.state != "offer_accepted":
                raise UserError("Accept an offer first")
            record.state = "sold"
        return True
    
    def action_mark_property_cancelled(self):
        for record in self:
            record.state = "cancelled"
        return True
