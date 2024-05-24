from dateutil.utils import today

from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError
from odoo.tools import float_compare
from odoo.tools.date_utils import add


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate base property model'
    _order = 'id desc'

    _sql_constraints = [
        ('check_positive_expected_price', 'CHECK (expected_price > 0)',
         'The expected price should be strictly positive'),
        ('check_positive_selling_price', 'CHECK (selling_price >= 0)', 'The selling price should be positive')
    ]

    name = fields.Char(
        required=True,
    )
    active = fields.Boolean(
        default=True,
    )
    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('canceled', "Canceled")
        ],
        default='new',
        required=True,
        copy=False,
    )

    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=add(today(), months=3),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(
        readonly=True,
        copy=False,
    )
    bedrooms = fields.Integer(
        default=2,
    )
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West")
        ],
    )

    buyer = fields.Many2one(
        'res.partner',
        copy=False,
    )
    salesman = fields.Many2one(
        'res.users',
        default=lambda self: self.env.user,
    )
    type_id = fields.Many2one(
        'estate.property.type',
    )
    tag_ids = fields.Many2many(
        'estate.property.tag',
    )
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
    )

    total_area = fields.Float(
        compute='_compute_total_area',
    )
    best_price = fields.Float(
        compute='_compute_best_offer',
    )

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        self.total_area = self.living_area + self.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        self.best_price = max(self.offer_ids.mapped('price'), default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.update({'garden_orientation': 'north', 'garden_area': 10})
        else:
            self.update({'garden_orientation': False, 'garden_area': 0})

    def action_set_canceled(self):
        self.state = 'canceled'

    def action_set_sold(self):
        if not self.offer_ids:
            raise UserError("You cannot sell a property without having received an offer!")
        self.state = 'sold'

    @api.constrains('selling_price')
    def check_selling_price(self):
        for record in self:
            if float_compare(record.selling_price / record.expected_price,
                             0.9, 2) < 0:
                raise ValidationError("The selling price cannot be lower than 90% of the expected price!")

    @api.ondelete(at_uninstall=False)
    def _unlink_verif(self):
        if self.filtered(lambda record: record.state not in ('new', 'canceled')):
            raise UserError("Can't delete a property which is not in state between 'new' and 'canceled'")
