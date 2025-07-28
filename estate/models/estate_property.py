from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Estate Module"
    _order = 'id desc'

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', "Expected price should be bigger than 0"),
        ('check_selling_price', 'CHECK(selling_price >= 0)', "Selling price should be 0 or bigger"),
    ]

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda _: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean(default=True)
    partner_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    user_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
    type_id = fields.Many2one('estate.property.type', string="Type")
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    total_area = fields.Float(compute='_compute_total_area')
    best_offer = fields.Float(compute='_compute_best_offer')
    garden_orientation = fields.Selection(
        selection=[
            ('orth', "North"),
            ('northeast', "North-East"),
            ('east', "East"),
            ('southeast', "South-East"),
            ('west', "West"),
            ('southwest', "South-West"),
            ('south', "South"),
            ('northwest', "North-West"),
        ],
    )
    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        default="new",
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for estate in self:
            estate.total_area = estate.living_area + estate.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for estate in self:
            estate.best_offer = max(estate.offer_ids.mapped('price'), default=0.0)

    @api.constrains('selling_price')
    def _check_sell_price(self):
        for estate in self:
            if float_is_zero(estate.selling_price, precision_rounding=2):
                continue
            if float_compare(estate.selling_price, estate.expected_price * 0.9, 2) == -1:
                raise ValidationError(_("Sell Price needs to be at least 90perc of Expected Price"))

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.ondelete(at_uninstall=False)
    def _unlink_only_new_or_cancelled(self):
        for estate in self:
            if estate.state not in ['new', 'cancelled']:
                raise UserError(_("Cannot delete properties that are not New or Cancelled"))

    def sell_property(self):
        for estate in self:
            if estate.state == 'cancelled':
                raise UserError(_("Cancelled property cannot be sold"))
            estate.state = 'sold'

    def cancel_property(self):
        for estate in self:
            if estate.state == 'sold':
                raise UserError(_("Sold property cannot be cancelled"))
            estate.state = 'cancelled'
