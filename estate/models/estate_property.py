from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare
from odoo.tools.translate import _

DEFAULT_GARDEN_AREA = 10


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property."
    _order = "id desc"

    active = fields.Boolean('Active', default=True)
    name = fields.Char('Real Estate Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Availability Date', copy=False, default=fields.Datetime.today() + relativedelta(months=+3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
    )
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        required=True,
        copy=False,
        default='new',
    )
    total_area = fields.Integer(compute='_compute_total_area', string='Total Area (sqm)')
    best_price = fields.Float(compute='_compute_best_price', string='Best Price')
    sales_person_id = fields.Many2one('res.users', string='Salesman', index=True, default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False, readonly=True, compute='_compute_buyer')
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    type_id = fields.Many2one('estate.property.type', string='Type', required=True)

    ## CONSTRATINS ##
    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price must be strictly positive.',
    )

    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price must be positive.',
    )

    @api.constrains('expected_price', 'selling_price')
    def _check_expected_vs_selling_price_ratio(self):
        for property in self:
            if any(offer.status == 'accepted' for offer in property.offer_ids):
                if float_compare(property.selling_price, property.expected_price * 0.9, precision_digits=2) < 0:
                    raise ValidationError(_('The selling price cannot be lower than 90 precent of the expected price: \n Selling Price: %s, Expected Price: %s') % (property.selling_price, property.expected_price))

    @api.depends('offer_ids.price')
    def _compute_selling_price(self):
        for property in self:
            property.selling_price = self.offer_ids.price

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    @api.depends('offer_ids.status')
    def _compute_buyer(self):
        for record in self:
            for offer in record.offer_ids:
                if offer.status == 'accepted':
                    record.buyer_id = offer.partner_id
                    return
            record.buyer_id = None

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = DEFAULT_GARDEN_AREA
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_cancel_property(self):
        if self.state == 'sold':
            raise UserError(_('Sold properties cannot be canceled.'))
        self.state = 'cancelled'
        for offer in self.offer_ids:
            offer.status = None
        return True

    def action_sold_property(self):
        if self.state == 'cancelled':
            raise UserError(_('Cancelled properties cannot be sold.'))
        self.state = 'sold'
        return True

    @api.ondelete(at_uninstall=False)
    def _unlink_except_new_or_cancelled(self):
        for record in self:
            if record.state not in ('new', 'cancelled'):
                raise UserError(_('You cannot delete a property unless its state is `New` or `Cancelled`.'))
