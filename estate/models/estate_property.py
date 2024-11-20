from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Estate Property"
    _order = "id desc"
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0)',
         "The property expected price must be strictly positive."),
        ('check_selling_price', 'CHECK(selling_price >= 0)',
         "The property selling price must be positive."),
    ]

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False,
                                    default=lambda self: fields.Date.today() + relativedelta(months=3),
                                    string="Available From")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(copy=False, default='new', required=True, string="Status",
                             selection=[
                                 ('new', "New"),
                                 ('offer_received', "Offer Received"),
                                 ('offer_accepted', "Offer Accepted"),
                                 ('sold', "Sold"),
                                 ('cancelled', "Cancelled"),
                             ]
                             )
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer")
    salesman_id = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string="Property Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Float(compute='_compute_total_area', string="Total Area (sqm)")
    best_price = fields.Float(compute='_compute_best_price', string="Best Offer")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if (not float_is_zero(record.selling_price, precision_digits=2) and
                    float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) < 0):
                raise ValidationError(self.env._("The selling price must be at least 90% of the expected price."))

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.ondelete(at_uninstall=False)
    def prevent_delete(self):
        for record in self:
            if record.state not in ('new', 'cancelled'):
                raise UserError(self.env._("Only new and cancelled properties can be deleted."))

    def action_set_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(self.env._("Cancelled properties cannot be sold."))
            record.state = 'sold'
        return True

    def action_set_cancelled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(self.env._("Sold properties cannot be cancelled."))
            record.state = 'cancelled'
        return True

    def accept_offer(self, accepted_offer):
        if self.state == 'offer_accepted':
            raise UserError(self.env._("An offer has already been accepted."))
        self.state = 'offer_accepted'
        self.buyer_id = accepted_offer.partner_id
        self.selling_price = accepted_offer.price
        accepted_offer.status = 'accepted'

        # Refuse other offers
        for offer in self.offer_ids:
            if offer != accepted_offer:
                offer.status = 'refused'

    def check_new_offer(self, offer_price):
        self.state = 'offer_received'
        if offer_price < min(self.offer_ids.mapped('price'), default=0):
            raise UserError(self.env._("The offer price is less than the others."))
        return True
