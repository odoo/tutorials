from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError
from odoo.tools import float_is_zero, float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Property Name', required=True, translate=True)
    description = fields.Text('Property Description', required=True)
    date_availability = fields.Date('Date Availability', copy=False,
                                    default=lambda self: fields.Date.today() + timedelta(days=3))
    postcode = fields.Char('Postal Code')
    selling_price = fields.Float('Selling Price', readonly=True, copy=False, default=0.00)
    expected_price = fields.Float('Expected Price', required=True)
    bedrooms = fields.Integer('No of. Bedrooms', default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage', default=False)
    garden = fields.Boolean('Garden', default=False)
    garden_area = fields.Integer('Garden Area(sqm)')
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        string='Garden Orientation',
    )
    total_area = fields.Integer('Total Area(sqm)', compute='_compute_total_area')
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        string='State',
        default='new',
        required=True,
        copy=False,
        tracking=True,
    )
    property_type_id = fields.Many2one("estate.property.type", string='Property Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    property_tag_ids = fields.Many2many('estate.property.tag', string='Property Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    best_price = fields.Float('Best Offer', compute='_compute_best_offer')

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price of a property must be positive',
    )

    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price of a property must be positive',
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price_percentage(self):
        if (
                not float_is_zero(self.selling_price, precision_digits=2)
                and float_compare(self.selling_price, (self.expected_price * (90 / 100)), precision_digits=2) == -1
        ):
            raise ValidationError("The selling price cannot be lower than 90% of the expected price.")

    @api.ondelete(at_uninstall=False)
    def _unlink_property_if_new_or_cancelled(self):
        for record in self:
            if record.state not in ('new', 'cancelled'):
                raise UserError('Only new and cancelled state of property can be unlinked.')

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def write(self, vals):
        new_state = vals.get('state')

        match new_state:
            case 'offer_received':
                if not self.offer_ids:
                    raise ValidationError("A property must have at least one offer.")

            case 'offer_accepted':
                if not (self.offer_ids.filtered(lambda offer: offer.status == 'accepted')):
                    raise ValidationError("A property cannot be marked as 'Offer Accepted' without an accepted offer.")

            case 'cancelled':
                if self.state == 'sold':
                    raise ValidationError("This property has already been sold and cannot be cancelled.")

            case 'sold':
                if not (self.offer_ids.filtered(lambda offer: offer.status == 'accepted')):
                    raise ValidationError("A property cannot be marked as 'Offer Accepted' without an accepted offer.")
                if self.state == 'cancelled':
                    raise ValidationError("This property has already been cancelled and cannot be sold.")

        return super().write(vals)

    def action_cancel_property(self):
        self.ensure_one()
        self.state = 'cancelled'

    def action_sold_property(self):
        self.ensure_one()
        self.state = 'sold'
