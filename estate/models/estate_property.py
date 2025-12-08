from dateutil.relativedelta import relativedelta
from odoo import api, exceptions, fields, models
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'estate property module'
    _order = 'id desc'

    name = fields.Char(required=True)
    description = fields.Text("Description")
    date_availability = fields.Date(
        "Date Availability", default=fields.Date.today() + relativedelta(months=3), copy=False
    )
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", default=0, readonly=True, copy=False)
    bedrooms = fields.Integer(required=True, default=2)
    living_area = fields.Integer("Living Area (sqm)", required=True)
    facades = fields.Integer(default=0)
    garage = fields.Boolean(default=False)
    garden = fields.Boolean(default=False)
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection([('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')])
    total_area = fields.Integer("Total Area (sqm)", compute='_compute_total_area')
    postcode = fields.Integer()
    active = fields.Boolean(default=True)
    status = fields.Selection(
        [
            ('new', 'New'),
            ('offer received', 'Offer Received'),
            ('offer accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        default='new',
        copy=False,
    )
    estate_type_id = fields.Many2one(comodel_name='estate.property.type')
    estate_tag_ids = fields.Many2many(comodel_name='estate.property.tag')
    estate_offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    partner_id = fields.Many2one(comodel_name='res.partner')
    user_id = fields.Many2one(comodel_name='res.users', default=lambda self: self.env.user)
    best_offer = fields.Float(compute='_compute_best_price')
    _sql_constraints = [
        (
            'check_stricly_positive_expected_price',
            'CHECK(expected_price > 0)',
            'The expected price of an estate property must be strictly positive.',
        ),
        (
            'check_positive_selling_price',
            'CHECK(selling_price >= 0)',
            'The selling price of an estate property must be positive.',
        ),
    ]

    @api.constrains('selling_price', 'expected_price')
    def _check_valid_selling_price(self):
        for record in self:
            if not (any(offer.status == 'accepted' for offer in self.estate_offer_ids)):
                continue

            if float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) < 0:
                raise exceptions.ValidationError("The selling price must not be below 90 % of the expected price")

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('estate_offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if len(record.estate_offer_ids) == 0:
                record.best_offer = 0
            else:
                record.best_offer = max(record.estate_offer_ids.mapped('price'))

    @api.onchange('garden')
    def _onchange_partner_id(self):
        if self.garden:
            self.garden_orientation = 'north'
            self.garden_area = 10
        else:
            self.garden_orientation = None
            self.garden_area = 0

    def action_cancel(self):
        if self.status == 'sold':
            raise exceptions.UserError('A sold property cannot be cancelled')

        self.status = 'cancelled'

    def action_sold(self):
        if self.status == 'cancelled':
            raise exceptions.UserError('A cancelled property cannot be sold')

        self.status = 'sold'

    @api.ondelete(at_uninstall=False)
    def _unlink_if_estate_is_not_new_nor_cancelled(self):
        if any(estate.status!='new' and estate.status!='cancelled' for estate in self):
            raise exceptions.UserError('Can only delete new and cancelled records!')
