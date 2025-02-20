from odoo import api,fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate property details"
    _inherit = 'mail.thread'
    _order = "id desc"
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0)', 'Expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'Selling price must be positive.'),
        ('check_bedroom', 'CHECK(bedrooms >= 0)', ' Bedroom must be positive.'),
        ('check_living_area', 'CHECK(living_area >= 0)', 'Living_area must be positive.'),
        ('check_facades', 'CHECK(facades >= 0)', 'Facades must be positive.'),
        ('check_garden_area', 'CHECK(garden_area >= 0)', 'Garden_area must be positive.'),
    ]

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description", required=True)
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From", copy=False, default=fields.Date.add(fields.Date.today(), months=3)) 
    expected_price = fields.Float(string="Expected Price")
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False) 
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"), 
            ("south", "South"), 
            ("east", "East"), 
            ("west", "West")
        ]
    )
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        required=True,
        copy=False,
        default="new",
        group_expand=True
    )
    image = fields.Image("Image") 
    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_total_area")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")
    property_type_id = fields.Many2one(
        'estate.property.type', string="Property Type")
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson",default=lambda self: self.env.user)
    buyer_id = fields.Many2one(
        "res.partner", string="Buyer")
    tag_ids = fields.Many2many(
        "estate.property.tag", string="Tags")
    offer_ids = fields.One2many(
        "estate.property.offer", "property_id", string="Offers")
    company_id = fields.Many2one(
        "res.company", string="Company", default=lambda self: self.env.user.company_id,
        required=True)
    
    def property_action_cancel(self):
        for record in self:
            record.state = 'cancelled'

    def property_action_sell(self):
        for record in self:
            if record.state != "offer_accepted":
                raise UserError(
                    "Property can only be sold after offer is accepted."
                )
            record.state = 'sold'
    
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max((offer.price for offer in record.offer_ids), default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2): 
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) == -1:
                    raise models.ValidationError(
                        "The selling price cannot be lower than 90% of the expected price!"
                    )

    @api.ondelete(at_uninstall=False)
    def _unlink_if_property_is_new_or_cancelled(self):
        for record in self:
            if record.state not in ["new", "cancelled"]:
                raise UserError(
                    "You cannot delete a property unless its state is 'New' or 'Cancelled'."
                )
