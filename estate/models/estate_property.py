from dateutil.relativedelta import relativedelta

from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.tools import float_compare


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Estate property"

    _order = 'id desc'

    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True, string="Title", tracking=True)
    description = fields.Text(string="Description", tracking=True)
    postcode = fields.Char(required=True, string="Postcode", tracking=True)
    date_availability = fields.Date(required=True, default=lambda self: fields.Date.today() + relativedelta(months=+3), copy=False, string="Available From")
    expected_price = fields.Float(required=True, string="Expected Price", tracking=True)
    selling_price = fields.Float(readonly=True, copy=False, string="Selling Price")
    bedrooms = fields.Integer(required=True, default=2, string="Bedrooms")
    living_area = fields.Integer(required=True, string="Living Area (sqm)", help="Living area with a ceiling height of minimum 4 feet")
    facades = fields.Integer(required=True, string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden", inverse='_inverse_garden')
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection([
        ('north', "North"), ('south', "South"), ('east', "East"), ('west', "West")
    ], string="Garden Orientation")
    total_area = fields.Integer(store=True, compute='_compute_total_area', string="Total Area (sqm)")
    state = fields.Selection([
        ('new', "New"), ('offer_received', "Offer Received"), ('offer_accepted', "Offer Accepted"), ('sold', "Sold"), ('canceled', "Canceled")
    ], string="State", default='new', required=True, readonly=True, tracking=True)
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    seller_id = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    best_price = fields.Float(required=True, string="Best Price", readonly=True, compute='_compute_best_price')
    available_for_offers = fields.Boolean(store=False, compute='_compute_available_for_offers')
    color = fields.Integer(string="Color Index", default=0)

    _check_expected_price = models.Constraint(
        'CHECK (expected_price > 0)',
        "The expected price must be greater than 0."
    )
    _check_selling_price = models.Constraint(
        'CHECK (selling_price >= 0)',
        "The selling price must be greater or equal than 0."
    )

    @api.depends('living_area', 'garden_area', 'garden')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.onchange('garden')
    def _on_change_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = None

    def _inverse_garden(self):
        for record in self:
            if not record.garden:
                record.garden_area = 0
                record.garden_orientation = None

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price')) if len(record.offer_ids) > 0 else 0

    def action_mark_as_sold(self):
        for record in self:
            if record.state != 'offer_accepted':
                raise UserError(self.env._("Cannot mark a non offer_accepted property as sold"))

            if len(record.offer_ids.filtered(lambda offer: offer.status == 'accepted')) != 1:
                raise UserError(self.env._("Cannot mark a property as sold without an accepted offer"))

            record.state = 'sold'

    def action_mark_as_canceled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(self.env._("Cannot mark a sold property as canceled"))
            record.state = 'canceled'

    def compute_accepted_offer(self, offer):
        for record in self:
            if not record.available_for_offers:
                raise UserError(self.env._("Cannot add or update an offer on a property that is not available for offers"))

            record.selling_price = offer.price
            record.buyer_id = offer.partner_id
            record.state = 'offer_accepted'

    def compute_new_offer(self):
        for record in self:
            if not record.available_for_offers:
                raise UserError(self.env._("Cannot add or update an offer on a property that is not available for offers"))

            if record.state == 'new':
                record.state = 'offer_received'

    @api.depends('state')
    def _compute_available_for_offers(self):
        for record in self:
            record.available_for_offers = record.state in {'new', 'offer_received'}

    @api.constrains('selling_price', 'expected_price')
    def _check_prices(self):
        for record in self:
            if len(record.offer_ids.filtered(lambda x: x.status == 'accepted')) > 0 and float_compare(record.selling_price, record.expected_price * 0.9, 2) == -1:
                raise UserError(self.env._("The selling price must be at least 90% of the expected price"))

    @api.ondelete(at_uninstall=False)
    def _check_ondelete(self):
        for record in self:
            if record.state not in {'new', 'canceled'}:
                raise UserError(self.env._("Cannot delete a property that is not in the new or canceled state"))
