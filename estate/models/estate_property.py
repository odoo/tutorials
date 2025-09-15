from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property annoucements"
    _order = "id desc"

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "The expected price must be strictly positive.",
    )

    _check_selling_price = models.Constraint(
        "CHECK(selling_price > 0)",
        "The expected selling price must be positive.",
    )

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Availabile From", default=fields.Date.today() + relativedelta(months=3), copy=False)
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tags_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_total_area", string="Total Area")
    best_offer = fields.Float(compute="_compute_best_offer", string="Best Offer")
    state = fields.Selection(
        string='Status',
        default='new',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
    )
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for property in self:
            if not property.mapped('offer_ids.price'):
                property.best_offer = 0
            else:
                property.best_offer = max(property.mapped('offer_ids.price'))

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def cancel_property(self):
        for property in self:
            if property.state == 'sold':
                raise UserError("You cannot cancel a sold property.")
            else:
                property.state = 'cancelled'
        return True

    def sell_property(self):
        for property in self:
            if property.state == 'cancelled':
                raise UserError("You cannot sell a cancelled property.")
            else:
                property.state = 'sold'
        return True

    @api.constrains('selling_price', 'state', 'expected_price')
    def _check_selling_price(self):
        for property in self:
            if float_compare(property.selling_price, 0.9 * property.expected_price, precision_digits=2) < 0 and (property.state == 'sold' or property.state == 'offer_accepted'):
                raise ValidationError("the selling price cannot be lower than 90% of the expected selling price")

    @api.ondelete(at_uninstall=True)
    def unlink_check_state_of_property(self):
        if self.state not in ['new', 'cancelled']:
            raise ValidationError("Can't delete a property if its state is not 'New' or 'Cancelled'")
