from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _order = "id desc"
    
    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date Availability', copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float('Expected Price')
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area')
    total_area = fields.Integer(string="Total Area (sqm)", compute="_compute_total_area")
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], string='Garden Orientation')
    state = fields.Selection(selection=[
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ], string='State', default='new', copy=False)
    active = fields.Boolean('Active', default=True)
    
    salesman_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")

    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Name must be unique'),
        ('check_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be positive'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'Selling price must be positive'),
    ]

    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
            
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.mapped("offer_ids.price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.constrains('selling_price', 'expected_price')
    def _check_offer(self):
        for record in self:
            min_price = (record.expected_price or 0.0) * 0.90
            if not float_is_zero(record.selling_price, precision_digits=2) and float_compare(record.selling_price, min_price, precision_digits=2) <0:
                raise ValidationError(
                    "The selling price cannot be lower than 90% of the expected price. "
                    f"(Expected: {record.expected_price:.2f}, Minimum: {min_price:.2f})"
                )


    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_canceled(self):
        for record in self:
            if record.state not in ('new', 'canceled'):
                raise UserError(
                    f"Cannot delete property '{record.name}'. "
                    "Only properties in 'New' or 'Canceled' state can be deleted."
                )


    def action_cancel(self):
        if self.state == 'sold':
            raise UserError("Cannot cancel a sold property")
        self.state = 'canceled'
        return True
        
    def action_sold(self):
        if self.state == 'canceled':
            raise UserError("Cannot sell a canceled property")
        self.state = 'sold'
        return True
