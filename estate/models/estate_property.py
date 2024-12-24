from odoo import fields,api,models
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'real estate property'

    name = fields.Char(required=True) 
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy= False, default=lambda self: fields.Date.today() + timedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(default=0)
    garden_orientation = fields.Selection(
        selection=[
            ('north','North'),
            ('south','South'),
            ('east','East'),
            ('west','West')
        ],
        default='north'
    )
    active = fields.Boolean(default=True)
    state=fields.Selection(
        selection=[
            ('new','New'),
            ('offer_received','Offer Received'),
            ('offer_accepted','Offer Accepted'),
            ('sold','Sold'),
            ('cancelled','Cancelled')
        ],
        default='new', required=True
    )
    property_type_id =fields.Many2one('estate.property.type', string='real estate property type')
    partner_id = fields.Many2one('res.partner', string='Partner', copy=False)
    user_id = fields.Many2one('res.users', string='Users', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string='Tag')
    offer_ids = fields.One2many('estate.property.offer','property_id', string='Offer')
    total_area = fields.Float(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price', default=0.0)
    _order = "id desc"

    _sql_constraints = [('check_expected_price', 'CHECK(expected_price>=0)', 'Property expected price must be positive.'),
                        ('check_selling_price', 'CHECK(selling_price>=0)', 'Property selling price must be positive.')]
    
    @api.constrains('expected_price','selling_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2) :
                continue
            if float_compare(value1=record.selling_price,value2=(0.9*record.expected_price),precision_digits=2)==-1:
                raise ValidationError('The selling price must be atleast 90% of expected price')
 
    
    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
 
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'),default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        self.garden_area=10 if self.garden else 0
        self.garden_orientation='north' if self.garden else ""

    def action_set_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError('Cancelled Items can not be sold.')
            record.state = 'sold'
        return True
    
    def action_set_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('Sold Items can not be cancelled.')
            record.state = 'cancelled'
        return True
    

    @api.ondelete(at_uninstall=False)
    def prevent_deletion(self):
        for record in self:
            if record.state not in ('new', 'cancelled'):
                raise UserError('Only new or cancelled property can be deleted.')
