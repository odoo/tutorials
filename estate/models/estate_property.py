from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _
from odoo.tools.float_utils import float_compare, float_is_zero
from datetime import timedelta


def default_availability_date(recordset):
    return fields.Date.context_today(recordset) + timedelta(days=90)


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Advertisement module"
    _order = "id desc"

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date availability', copy=False, default=default_availability_date)
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('Selling price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], string='Garden orientation')
    total_area = fields.Integer('Total Area', compute='_compute_total_area')
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(selection=[
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ], string="State", default='new', required=True, copy=False)
    property_type_id = fields.Many2one('estate.property.type', string="Property type")
    property_buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    property_salesperson_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
    property_tag_ids = fields.Many2many('estate.property.tag', string="Property tags")
    property_offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    best_price = fields.Float('Best Price', compute='_compute_best_price')

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price must be strictly positive.'
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price must be positive.'
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('property_offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            offer_prices = record.property_offer_ids.mapped('price')
            record.best_price = max(offer_prices) if offer_prices else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def check_create_offer(self, new_offer_price):
        for record in self:
            for offer in record.property_offer_ids:
                if new_offer_price < offer.price:
                    raise ValidationError(_("Cannot create an offer with a lower amount than an existing offer."))
            if record.state == 'new':
                record.state = 'offer_received'
        return True

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(_('Cancelled properties cannot be sold.'))
            record.state = 'sold'
        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_('Sold properties cannot be cancelled.'))
            record.state = 'cancelled'
        return True

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2) and float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) == -1:
                raise ValidationError(_('The selling price must be at least 90% of the expected price! You must reduce the expected price if you want to accept this offer.'))

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        for record in self:
            if not record.state in ['new', 'cancelled']:
                raise UserError(_(
                    'You cannot delete a property that is in %s state.',
                    dict(self._fields['state']._description_selection(self.env)).get(record.state)
                ))
