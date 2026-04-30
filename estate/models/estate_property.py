from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "estate property used to buy and sell houses"
    _order = 'id desc'

    _check_expected_price = models.Constraint(
        'CHECK (expected_price >= 0)',
        'The expected price cannot be negative',
    )

    _check_selling_price = models.Constraint(
        'CHECK (selling_price >= 0)',
        'The Selling price must be positive'
    )

    name = fields.Char(required=True)
    description = fields.Text()
    facades = fields.Integer()
    postcode = fields.Char()
    sequence = fields.Integer(default=1)

    garage = fields.Boolean()
    bedrooms = fields.Integer(default=2)
    garden = fields.Boolean()
    living_area = fields.Integer()
    garden_area = fields.Integer()
    total_area = fields.Integer(compute="_compute_total_area")
    garden_orientation = fields.Selection(
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ],
    )

    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    best_price = fields.Float(compute='_compute_best_price', store=True)
    date_availability = fields.Date(
        default=lambda self: fields.Date.add(fields.Date.context_today(self), months=3),
        copy=False
    )

    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        default='new',
        copy=False,
        required=True,
    )

    buyer_id = fields.Many2one('res.partner', copy=False)
    salesperson_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    property_type_id = fields.Many2one('estate.property.type')
    image = fields.Image()
    is_favorite = fields.Boolean()

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0.0)

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, 2):
                continue
            if float_compare(record.selling_price, record.expected_price * 0.9, 2) < 0:
                raise ValidationError(_("The Selling price cannot be lower than 90% of the expected price"))

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _unlink_except_new_cancelled_properties(self):
        if self.state not in ['new', 'cancelled']:
            raise UserError(_("You can only delete Properties that are only new and cancelled"))

    def action_set_sold(self):
        if self.state == 'cancelled':
            raise UserError(_("You cannot sell an offer that is already Cancelled"))
        self.state = 'sold'
        return {
            'effect': {
                'type': 'rainbow_man',
                'message': _("Huge congrats on selling your property! Here's to new beginnings!")
            }
        }

    def action_set_cancelled(self):
        if self.state == 'sold':
            raise UserError(_("You cannot cancel an offer that is already Sold"))
        self.state = 'cancelled'
        return True

    def action_reset(self):
        if self.state == 'sold':
            self.state = 'offer_accepted'
        elif self.state == 'cancelled':
            offers = self.offer_ids.filtered(lambda r: r.status == 'accepted')
            if offers:
                self.state = 'offer_accepted'
            elif self.offer_ids:
                self.state = 'offer_received'
            else:
                self.state = 'new'
        return True

    def action_accept_best(self):
        for rec in self:
            best_offer = rec.offer_ids.sorted('price', reverse=True)[:1]
            best_offer.action_accept()
        return True
