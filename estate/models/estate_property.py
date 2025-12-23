from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class Property(models.Model):
    _name = "estate.property"
    _description = "Real Estate property"
    _order = "id desc"

    name = fields.Char('Title', required=True, default='Unknown')
    active = fields.Boolean('Active', default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('received offer', 'Received offer'),
        ('offer accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ], string='Status', required=True, copy=False, default='new')
    description = fields.Text('Description')
    last_seen = fields.Datetime("Last Seen", default=lambda self: fields.Datetime.now())
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available from', copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('Selling price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden area (sqm)')
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], string='Garden Orientation')
    total_area = fields.Integer(compute="_compute_total_area")
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    salesperson_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    best_price = fields.Float(compute="_compute_best_price")

    # Functions
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0

    @api.onchange('garden')
    def _onchange_partner(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    @api.ondelete(at_uninstall=False)
    def _unlink_if_property_new_or_cancelled(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError(f"Can\'t delete property '{record.name}' if state is not New or Cancelled")

    def action_sell_property(self):
        for record in self:
            if record.state == 'cancelled':
                msg = "Cancelled properties cannot be sold."
                raise UserError(msg)
            record.state = 'sold'
        return True

    def action_cancel_property(self):
        for record in self:
            if record.state == 'sold':
                msg = "Sold properties cannot be cancelled."
                raise UserError(msg)
            record.state = 'cancelled'
        return True

    # Constraints
    _check_expected_price = models.Constraint('CHECK (expected_price > 0)', "A property expected price must be strictly positive")
    _check_selling_price = models.Constraint('CHECK (selling_price >= 0)', "A property selling price must be positive")

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price_percentage(self):
        for record in self:
            if record.state == 'offer accepted' and float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=9) == -1:
                msg = "The selling price cannot be lower than 90% of the expected price"
                raise ValidationError(msg)
