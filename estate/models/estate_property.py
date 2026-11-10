from dateutil.relativedelta import relativedelta
from datetime import date
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class EstatePropertyModel(models.Model):
    _name = 'estate.property'
    _description = "Real Estate property database"
    _order = 'id desc'
    _expected_price_check = models.Constraint('CHECK(expected_price > 0)', "The expected price must be strictly positive.")
    _selling_price_check = models.Constraint('CHECK(selling_price >= 0)', "The selling price must be positive.")

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    active = fields.Boolean(default=True)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', "North"),
            ('east', "East"),
            ('south', "South"),
            ('west', "West"),
        ],
        string="Garden Orientation",
        default='south',
    )
    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancel', "Cancelled"),
        ],
        required=True,
        copy=False,
        default='new',
    )

    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        'res.users',
        string="Salesperson",
        default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

    total_area = fields.Integer(compute='_compute_total_area', string="Total Area (sqm)")
    best_price = fields.Float(compute='_compute_best_price', string="Best Offer")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            if prices:
                record.best_price = max(prices)
            else:
                record.best_price = 0.0

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
                    raise ValidationError(self.env._("The selling price cannot be lower than 90% of the expected price!"))

    @api.ondelete(at_uninstall=False)
    def _ondelete_property(self):
        for record in self:
            if record.state not in ['new', 'cancel']:
                raise UserError(self.env._("Only new or cancelled properties can be deleted!"))

    def action_sold(self):
        for record in self:
            if record.state == "cancel":
                raise UserError(self.env._("Canceled properties cannot be sold."))
            record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError(self.env._("Sold properties cannot be canceled."))
            record.state = "cancel"
        return True
