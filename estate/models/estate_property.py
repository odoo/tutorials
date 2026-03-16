from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Test Model for real estate'
    _check_positive_expected_price = models.Constraint(
        'CHECK (expected_price >= 0)', 'expected_price should be positive'
    )
    _check_positive_selling_price = models.Constraint(
        'CHECK (selling_price >= 0)', 'selling_price should be positive'
    )
    _order = 'id desc'

    name = fields.Char(default='Unknown')
    last_seen = fields.Datetime('Last Seen', default=fields.Datetime.now)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=fields.Date.add(fields.Date.today(), months=3)
    )
    expected_price = fields.Float()
    selling_price = fields.Float(copy=False, readonly=True, default=0)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    state = fields.Selection(
        string='status',
        selection=[
            ('new', "New"),
            ('offer received', "Offer Received"),
            ('offer accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        default='new',
        compute='_compute_statusbar',
        store=True,
    )
    active = fields.Boolean(default=True)
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='garden orientation direction',
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ],
    )
    property_type_id = fields.Many2one('estate.property.type')
    salesperson_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        index=True,
        default=lambda self: self.env.user,
    )
    buyer_id = fields.Many2one('res.partner', default='None', copy=False)
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='offers')
    total_area = fields.Float(compute='_compute_total_area')
    max_offer_price = fields.Float(
        default=None, compute='_compute_max_offer_price', store=True
    )
    estate_maintainance_id = fields.One2many(
        'estate.maintainance.request', 'property_id'
    )
    visit_ids = fields.One2many('estate.property.visit', 'property_id', string='visits')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    def button_cancel(self):
        if self.state == 'cancelled':
            raise UserError('The property is already cancelled')
        elif self.state == 'sold':
            raise UserError('The property is already sold, you cannot cancel it')
        else:
            self.state = 'cancelled'

    def button_sold(self):
        if self.state == 'sold':
            raise UserError('The property is already sold')
        elif self.state == 'cancelled':
            raise UserError('The property is already cancelled, and cannot be sold')
        else:
            self.state = 'sold'

    @api.depends('offer_ids.price')
    def _compute_max_offer_price(self):
        if self.offer_ids:
            new_max_offer_price = max(self.offer_ids.mapped('price'))
            if self.max_offer_price != new_max_offer_price:
                self.max_offer_price = new_max_offer_price

    def accept_best_offer(self):
        for offers in self.offer_ids:
            if self.max_offer_price == offers.price:
                offers.action_accept_offer()
                ##################################
                # old code
                # offers.status = 'accepted'
                # self.state = 'offer accepted'
                # self.buyer_id = offers.partner_id
                # self.selling_price = offers.price
                ##################################
            else:
                offers.status = 'refused'

    @api.depends('offer_ids')
    def _compute_statusbar(self):
        for record in self:
            if record.offer_ids and record.state == 'new':
                record.state = 'offer received'

    @api.constrains('selling_price', 'expected_price')
    def check_percentage(self):
        for record in self:
            if record.selling_price and record.expected_price:
                if (
                    float_compare(
                        record.selling_price,
                        record.expected_price * 0.9,
                        precision_digits=1,
                    )
                    < 0
                ):
                    raise ValidationError(
                        'the selling perice cant be less than 90% of the expected price'
                    )

    @api.ondelete(at_uninstall=False)
    def _unlink_if_user_inactive(self):
        for record in self:
            if record.state not in ['cancelled','new']:
                raise UserError('cannot delete - only delete from the state `new` and `cancelled`')
