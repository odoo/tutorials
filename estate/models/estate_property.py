from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero
from odoo.tools import _


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = "id desc"

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Availability Date', copy=False, 
        default=fields.Datetime.add(fields.Datetime.today(), days=7))
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage Available')
    garden = fields.Boolean(string='Has Garden')
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string='Garden Orientation'
    )

    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        string='State', default='new', copy=False, required=True
    )

    property_type_id = fields.Many2one('estate.property.type', string='Type')

    salesperson_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one(
        'res.partner', 
        string='Buyer', 
        copy=False
    )

    property_tag_ids = fields.Many2many('estate.property.tag', string='Tag')

    property_offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offer')

    total_area = fields.Integer(string='Total Area', compute='_compute_total_area')
    currency_id = fields.Many2one('res.currency', string='Currency')
    best_price = fields.Monetary(string='Best Offer', compute='_compute_best_price')

    _sql_constraints = [
        ('expected_price_positive', 'CHECK(expected_price > 0)', 'A property expected price must be strictly positive.'),
        ('selling_price_positive', 'CHECK(selling_price > 0)', 'A property selling price must be positive.')
    ]

    @api.constrains('selling_price', 'expected_price')
    def _check_price(self):
        for property in self:
            too_low = float_compare(property.selling_price, 0.9 * property.expected_price, precision_rounding=0.01) == -1
            if not float_is_zero(property.selling_price, precision_rounding=0.01) and too_low:
                raise UserError("Offer can't be lower than 90% of the expected price.")


    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('property_offer_ids.price')
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.property_offer_ids.mapped('price'), default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 20
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_sold(self):
        if any(property.state == 'cancelled' for property in self):
            raise UserError(_("A cancelled property cannot be sold."))
        property.state = 'sold'
        return True

    def action_cancel(self):
        for property in self:
            if property.state == 'sold':
                raise UserError("A sold property cannot be cancelled.")
            property.state = 'cancelled'
        return True

    @api.ondelete(at_uninstall=False)
    def _unlink_except_reserved_property(self):
        for property in self:
            if property.state not in ['new', 'cancelled']:
                raise UserError("You can only delete properties in 'New' or 'Cancelled' state.")
    