from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Properties'
    _order = 'id desc '
    _inherit = ['mail.thread',
                'mail.activity.mixin',
                ]

    name = fields.Char("Title", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_available = fields.Date("Date Available", copy=False,
                                 default=lambda x: fields.Date.today() + relativedelta(month=3))
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West")
        ]
    )
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled")],
        copy=False,
        required=True,
        default='new',
    )
    partner_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    user_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.uid)
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    total_area = fields.Integer("Total Area", compute='_compute_total_area')
    best_price = fields.Float("Best Price", compute='_compute_best_price', default=0)

    _sql_constraints = [
        ('positive_expected_price', 'CHECK(expected_price > 0)',
         'The expected price must be greater than 0.'),
        ('positive_selling_price', 'CHECK(selling_price >= 0)',
         'The selling price must be greater than or equal to 0.'),
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property in self:
            prices = property.offer_ids.filtered(lambda x: x.status != 'refused').mapped('price')
            property.best_price = max(prices, default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        for property in self:
            if not property.garden:
                property.garden_area = 0
                property.garden_orientation = False
            else:
                property.garden_area = 10
                property.garden_orientation = 'north'

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for property in self:
            if (float_compare(property.selling_price, 0, precision_rounding=3) > 0
                    > float_compare(property.selling_price, property.expected_price * 0.9, precision_rounding=3)):
                raise ValidationError(_("Selling price cannot be lower than 90% of expected price"))

    @api.ondelete(at_uninstall=False)
    def _ondelete(self):
        for property in self:
            if property.state not in ['new', 'cancel']:
                raise UserError(_("Only new properties and cancelled properties can be deleted"))

    def action_property_sold(self):
        for property in self:
            if property.state != 'offer_accepted':
                raise UserError(_('Only properties with an accepted offer can be sold!'))
            property.state = 'sold'

    def action_property_cancel(self):
        for property in self:
            if property.state == 'sold':
                raise Warning(_('Sold properties cannot be cancelled!'))
            property.state = 'cancelled'

    def accept_offer(self, offer):
        self.ensure_one()
        self.state = 'offer_accepted'
        self.selling_price = offer.price
        self.partner_id = offer.partner_id.id
        for offer in self.offer_ids:
            if not offer.status:
                offer.status = "refused"

    def action_cancel(self):
        state = self.state
        if state != 'cancelled':
            self.state = 'cancelled'
