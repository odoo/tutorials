from odoo import api, fields, models, exceptions
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_compare, float_is_zero
from odoo.exceptions import ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "its just an estate property"
    _order = "id desc"

    # Basic fields
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=fields.Date.today()+ relativedelta(months=3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        )
    active = fields.Boolean(default=True)

    state = fields.Selection(
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        required=True,
        copy=False,
        default='new')

    # Relational fields
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    sales_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    # Computed fields
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_offer", default=0)

    # Constraints
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The expected price of a property should be strictly positive'),
         ('check_selling_price', 'CHECK(selling_price >= 0)',
         'The selling price of a property should be positive')
    ]

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0:
                    raise ValidationError("The selling price cannot be less than 90% of the expected price")

    # Compute Methods
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    # On Changes
    @api.onchange('garden')
    def _onchange_garden(self):
        # set default
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'

        # clear values
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # CRUD methods
    @api.ondelete(at_uninstall=False)
    def _chek_state(self):
        for record in self:
             if record.state in ['new', 'canceled']:
                raise exceptions.UserError("A property must be newly created or canceld to be deleted")

    # Buttons methods
    def set_canceled(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError("Sold properties cannot be canceled")

            record.state = 'canceled'
        return True

    def set_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise exceptions.UserError("Canceled properties cannot be sold")

            record.state = 'sold'
        return True
