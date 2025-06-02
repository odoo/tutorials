from dateutil.relativedelta import relativedelta
from odoo import fields, models, api, exceptions, tools


class Property(models.Model):
    _name = 'estate.property'
    _description = 'this is a estate_property'
    _order = 'id desc'

    name = fields.Char(string='Title', required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    state = fields.Selection(
        required=True,
        selection=[
            ('new', 'New'),
            ('received', 'Offer Received'),
            ('accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')],
        default="new",
        copy=False
    )
    active = fields.Boolean(default=True)
    property_type = fields.Many2one('estate.property.type')
    salesperson_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', copy=False)
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Integer(compute='_compute_area')
    best_price = fields.Float(compute='_compute_best_price')

    _sql_constraints = [
        ('check_expected_price_strictly_positive', 'CHECK (expected_price > 0)', "The expected price must be strictly positive."),
        ('check_selling_price_positive', 'CHECK (selling_price >= 0)', "The selling price must be positive.")]

    @api.depends('garden_area', 'living_area')
    def _compute_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=None)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    @api.onchange('offer_ids')
    def _onchange_offer_ids(self):
        if self.state == 'new' and len(self.offer_ids) > 0:
            self.state = 'received'

    def sold_button_action(self):
        for record in self:
            if record.state == 'cancelled':
                raise exceptions.UserError("Cancelled properties cannot be sold")
            record.state = 'sold'

    def cancel_button_action(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError("Sold properties cannot be cancelled")
            record.state = 'cancelled'

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price_minimum_threshold(self):
        for record in self:
            if tools.float_utils.float_is_zero(record.selling_price, precision_rounding=.01):
                continue
            if tools.float_utils.float_compare(record.expected_price * .9, record.selling_price, precision_rounding=.01) > 0:
                raise exceptions.ValidationError("The selling price should be at least 90% of the expected price."
                                                 "Lower the expected price if you want to accept the offer.")

    @api.ondelete(at_uninstall=False)
    def _check_state(self):
        for record in self:
            if record.state not in ('new', 'cancelled'):
                raise exceptions.UserError("Only new and cancelled propoerties can be deleted!")
