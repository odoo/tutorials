from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Handle real estate property'
    _sql_constraints = [
        ('check_price', 'CHECK(expected_price > 0)', "A property expected price must be strictly positive."),
        ('check_selling_price', 'CHECK(selling_price >= 0)', "A property selling price must be positive"),
    ]

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, string="Available From", default=fields.Date.today)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='Status',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'),
                   ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        required=True,
        copy=False,
        default='new',
    )
    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one("res.partner", copy=False)
    user_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    tags_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_offer", string="Best Offer")
    
    
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            record.best_price = max(self.offer_ids.mapped('price'), default=0)
            
    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for propert in self:
            if not float_is_zero(propert.selling_price, 2) and float_compare(propert.selling_price, 0.9*propert.expected_price, 2) < 0:
                raise ValidationError('The selling price cannot be lower tan 90% of the expected price')
            
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = False
            self.garden_orientation = False
            
    
    def action_set_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Canceled properties can't be sold.")
            record.state = 'sold'
        return True
    
    def action_set_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties can't be cancelled.")
            record.state = 'cancelled'
        return True
