from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = "estate.property"
    _inherit = ['mail.thread']
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char("Property Name", required=True)
    active = fields.Boolean(default=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postal Code")
    date_availability = fields.Date(
        "Availability Date",
        copy=False,
        default= lambda self: fields.Datetime.now() + relativedelta(months=3)
    )
    image = fields.Image("Property Image")
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Number of bedrooms", default=2)
    living_area = fields.Float("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Float("Garden Area (sqm)")
    company_id = fields.Many2one(
        "res.company",
        string="company",
        required=True,
        default=lambda self: self.env.company
    )
    buyer = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False
    )
    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Property Tag"
    )
    property_type_id = fields.Many2one(
        'estate.property.type',
        string="Property Type"
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers"
    )
    user_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user
    )
    garden_orientation = fields.Selection(
        selection = [
            ('north', 'North'),
            ('south', 'South'),
            ('west', 'West'),
            ('east', 'East')
        ]
    )
    state = fields.Selection(
        selection = [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        required=True, copy=False, default="new"
    )
    total_area = fields.Float("Total Area(sqm)", compute="_compute_total_area")
    best_price = fields.Float("Best Price", compute="_compute_best_price")

    _sql_constraints = [
        ('check_expected_price', 'check(expected_price > 0.0)', 'The Expected price should be greater than 0'),
        ('check_selling_price', 'check(selling_price >= 0.0)', 'The selling cannot be negative'),
        ('unique_property_type', 'unique(name)', 'Property Name should be unique')
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            max_price=0
            for offer in record.offer_ids:
                if offer.price > max_price:
                    max_price = offer.price
            record.best_price = max_price

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'

    def sell_property(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Cancelled properties cannot be sold")
            else:
                record.state = 'sold'

    def cancelled_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be cancelled")
            else:
                record.state = 'cancelled'

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, 2):
                continue

            min_expected_price = 0.9 * record.expected_price
            if float_compare(record.selling_price, min_expected_price, 2) == -1:
                raise ValidationError("The selling price should be atleast 90% of the expected price")

    @api.ondelete(at_uninstall=False)
    def _unlink_except_new_or_cancelled(self):
        for record in self:
            if record.state not in ('new', 'cancelled'):
                raise UserError("You cannot delete this property as it is neither in new or cancelled state")
