from odoo import api, models, fields
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    _sql_constraints = [
        (
            'positive_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be strictly positive'
        ), 
        (
            'positive_selling_price', 'CHECK(selling_price > 0)', 'Selling_price must be strictly positive'
        ),
    ]

    # Property name, description, Postal code, Availability date
    name = fields.Char(required=True, help='Name')
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False,default=fields.Datetime.today() + timedelta(days=90), readonly=True)

    # Price-related fields
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)

    #  Key details of the Property
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer()

    # Garden orientation selection
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
        string="Garden Orientation",
    )

    active = fields.Boolean(default=False)

    #  Property state
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="State", required=True, copy=False, default="new",
    )

    # Many2one Models for Property Type
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner",string="Buyer" , copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson" , default=lambda self: self.env.user)

    # Many2many Models for Property Tag
    tag_ids=fields.Many2many(string="Tags", comodel_name="estate.property.tag")

    # One2Many Models for Property Offer
    offer_ids = fields.One2many('estate.property.offer', 'property_id')

    total_area = fields.Float(compute='_compute_total_area')
    best_price=fields.Integer(compute="_compute_best_price")
    company_id = fields.Many2one(string="Company", comodel_name="res.company", default=lambda self: self.env.user.company_id)

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        """Calculates the total area by adding living and garden areas."""
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        """Finds the highest offer price among all offers."""
        for record in self:
            if record.offer_ids:
             record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0


    @api.onchange("garden")
    def _onchange_garden_availability(self):
        """Automatically set garden area and orientation when the garden is added or removed."""
        if self.garden:
            self.garden_area=10
            self.garden_orientation="north"
        else:
            self.garden_area=0
            self.garden_orientation=""
    
    def action_mark_property_sold(self):
        """Marks the property as sold unless it is cancelled."""
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled properties cannot be sold")
            record.state = "sold"
        return True

    def action_mark_property_cancelled(self):
        """Marks the property as cancelled unless it is already sold."""
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties cannot be cancelled")
            record.state = "cancelled"
        return True

    @api.constrains("selling_price", "expected_price")
    def _check_valid_selling_price(self):
        """Ensures the selling price is at least 90% of the expected price."""
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2) and float_compare(record.selling_price, record.expected_price*0.9, precision_digits=2) < 0:
                raise ValidationError("Selling price must be atleast 90% of the expected price")

    @api.ondelete(at_uninstall=False)
    def _prevent_delete(self):
        """Prevents deletion of properties unless they are new or cancelled."""
        for record in self:
            if record.state not in["new", "cancelled"]:
                raise UserError("You can only delete new or cancelled properties!")
