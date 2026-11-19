from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property test model'
    _order = "id desc"

    def _get_availability_default():
        today = fields.Date.today()
        return fields.Date.add(today, months=3)

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available from", copy=False, default=_get_availability_default())
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('west', 'West'),
        ('south', 'South'),
        ('east', 'East')
    ])
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('received', 'Offer Received'),
            ('accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        required=True,
        readonly=True,
        default='new'
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    user_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    type_id = fields.Many2one("estate.property.type", string="Property Type")
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area (sqm)")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    ####################################################
    # CONSTRAINTS
    ####################################################

    _strictly_positive_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price must be a positive value'
    )

    _positive_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price cannot be a negative value'
    )

    @api.constrains('selling_price')
    def _check_valid_selling_price(self):
        for record in self:
            if (
                float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0
                and not float_is_zero(record.selling_price, precision_digits=2)
            ):
                raise ValidationError("The accepted offer price should never be under 90% of the selling price")

    ####################################################
    # COMPUTE METHODS
    ####################################################

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    ####################################################
    # ONCHANGE METHODS
    ####################################################

    @api.onchange("garden")
    def _onchange_garden(self):
        for property in self:
            if property.garden:
                property.garden_orientation = property.garden_orientation or 'north'
                property.garden_area = property.garden_area or 10
            else:
                property.garden_orientation = None
                property.garden_area = None

    @api.onchange("garden_orientation", "garden_area")
    def _onchange_garden_info(self):
        for property in self:
            if not (property.garden_orientation and property.garden_area):
                property.garden = False

    ## On offer received move state
    @api.onchange("offer_ids")
    def _onchange_offers(self):
        for property in self:
            if property.offer_ids:
                property.state = 'received'

    ####################################################
    # ACTIONS
    ####################################################

    def cancel_property(self):
        for property in self:
            if property.state == 'sold':
                raise UserError(self.env._("You cannot set a previously sold property as Cancelled"))
            property.state = "cancelled"
            property.active = 0
        return True

    def sell_property(self):
        for property in self:
            if property.state == 'cancelled':
                raise UserError(self.env._("You cannot set a previously cancelled property as Sold"))
            property.state = "sold"
        return True
