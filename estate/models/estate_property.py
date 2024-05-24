from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.date_utils import add
from odoo.tools.translate import _
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "estate properties"
    _sql_constraints = [
        (
            'check_strictly_positive_expected_price',
            'CHECK(expected_price > 0)',
            "Expected Price must be strictly positive",
        ),
        (
            'check_positive_selling_price',
            'CHECK(selling_price >= 0)',
            "Selling Price must be positive",
        ),
    ]
    _order = 'id desc'

    name = fields.Char("Title", required=True)
    description = fields.Text()
    postcode = fields.Integer()
    date_availability = fields.Date(
        "Available from", copy=False, default=add(fields.Date.today(), months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('canceled', "Canceled"),
        ],
        required=True,
        default='new',
        copy=False,
    )

    property_type_id = fields.Many2one('estate.property.type', string="Property Types")
    user_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', inverse_name="property_id")

    total_area = fields.Integer("Total Area (sqm)", compute='_compute_total_area')
    best_price = fields.Float("Best Offer", compute='_compute_best_price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        self.garden_area, self.garden_orientation = (10, 'north') if self.garden else (0, None)

    def action_sell(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError(_('Can\'t sell canceled estate'))
            record.state = 'sold'
        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_('Can\'t cancel sold estate'))
            record.state = 'canceled'
        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if (
                not (float_is_zero(record.selling_price, precision_rounding=0.1))
                and float_compare(
                    record.selling_price, record.expected_price * 0.9, precision_rounding=0.1
                )
                < 0
            ):
                raise ValidationError(
                    _('Selling price can\'t be lower than 90% of the expected price')
                )
