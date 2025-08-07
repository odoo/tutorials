from datetime import date, timedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Manage real estate properties, including pricing, availability, features and buyer/seller information."
    _order = "id desc"

    _sql_constraints = [
        ('check_expected_price_positive', 'CHECK(expected_price > 0)', 'Expected price must be strictly positive.'),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)', 'Selling price must be zero or positive.')
    ]

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: date.today() + timedelta(days=90)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    best_price = fields.Float(compute="_compute_best_price")
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    living_area = fields.Float(string="Living Area (m²)")
    garden_area = fields.Float(string="Garden Area (m²)")
    total_area = fields.Float(compute="_compute_total_area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        help="Direction of the garden"
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        required=True,
        copy=False,
        default='new'
    )
    property_type = fields.Many2one("estate.property.type", string="Property Type")
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    seller = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    company_id = fields.Many2one(
        'res.company',
        string="Company",
        required=True,
        default=lambda self: self.env.company
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        self.check_access('write')
        for record in self:
            if record.state == 'cancelled':
                raise UserError(_("Cancelled properties cannot be sold."))
            if record.state == 'sold':
                raise UserError(_("The property is already sold."))
            if not record.offer_ids.filtered(lambda o: o.status == 'accepted'):
                raise UserError(_("You cannot sell a property without an accepted offer."))
            record.state = 'sold'

    def action_cancel(self):
        for record in self:
            if record.state in ['sold', 'cancelled']:
                raise UserError(_("You cannot cancel a sold or already cancelled property."))
            record.state = 'cancelled'

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price_margin(self):
        for record in self:
            if float_compare(record.selling_price, 0.0, precision_digits=2) > 0:
                min_acceptable_price = 0.9 * record.expected_price
                if float_compare(record.selling_price, min_acceptable_price, precision_digits=2) < 0:
                    raise ValidationError(_("Selling price cannot be lower than 90% of the expected price."))

    @api.ondelete(at_uninstall=False)
    def _check_property_state_on_delete(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError(_("Only properties with state 'New' or 'Cancelled' can be deleted."))
