from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

class Estateproperty(models.Model):
    _name = "estate.property"
    _description = "Estate property table"

    name = fields.Char('Property Name', required=True, default="unknown")

    property_type_id = fields.Many2one('estate.property.type', "Property Type")

    salesperson_id = fields.Many2one('res.users', string='Salesperson', default= lambda self: self.env.user)
    buyer_id= fields.Many2one('res.partner', string='Buyer', copy=False)

    tag_ids= fields.Many2many('estate.property.tag', "Tags")

    offer_ids = fields.One2many('estate.property.offer', 'property_id', 'Offers')

    description = fields.Text('Description', compute='_compute_desc')

    @api.depends("salesperson_id.name")
    def _compute_desc(self):
        for record in self:
            record.description = "Test for salesperson %s" % record.salesperson_id.name

    postcode= fields.Char('PostCode')
    date_availability= fields.Date('Available From',copy=False, default= lambda self: fields.Datetime.today() + timedelta(days=90))

    expected_price= fields.Float('Expected Price',required=True)
    selling_price= fields.Float('Selling Price',readonly=True, copy=False)

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive.'),
    ]

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < 0:
                raise ValidationError("The selling price must be positive.")
            
    @api.constrains('expected_price')
    def _check_expected_price(self):
        for record in self:
            if record.expected_price < 0:
                raise ValidationError("The expected price must be positive.")
            

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):  
                min_acceptable_price = record.expected_price * 0.9
                if float_compare(record.selling_price, min_acceptable_price, precision_digits=2) == -1:
                    raise ValidationError("The selling price cannot be lower than 90% of the expected price.")

    bedrooms= fields.Integer('Bedrooms',default=2)
    living_area= fields.Integer('Living Area')
    facades= fields.Integer('Facades')
    garage= fields.Boolean('Garage')
    garden= fields.Boolean('Garden')
    garden_area= fields.Integer('Garden Area')
    garden_orientation= fields.Selection(
        string='Type',
        selection=[('north', 'North'),('south', 'South'),('east', 'East'),('west', 'West')]
    )
    active = fields.Boolean(default=True)
    state= fields.Selection(
        string='State',
        selection=[('new', 'New'),('offered_rec', 'Offer recieved'),('offer_acc', 'Offer Accepted'),('sold', 'Sold'),('cancel', 'Cancelled')],
        required=True,
        copy=False,
        default='new'
        # compute = '_compute_offer_state'
        
    )

    #computed fields

    total_area = fields.Integer('Total Area', compute='_compute_total_area')

    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area


    best_price = fields.Float('Best Price', compute='_compute_best_price')

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property in self:
            prices = property.offer_ids.mapped('price')
            property.best_price = max(prices, default=0)

    #onchange
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False
        
    #object type and action

    def action_cancel(self):
        for property in self:
            if property.state== 'sold':
                raise UserError("A sold property cannot be cancelled.")
            else:
                property.state = 'cancel'

    def action_sold(self):
        for property in self:
            if property.state == 'cancel':
                raise UserError("A cancelled property cannot be sold.")
            if not property.offer_ids:
                raise UserError("Cannot sold without any offer.")
            else:
                property.state = 'sold'


    #offer recieved
    offer_recieved = fields.Boolean(compute="_compute_offer_recieved", store=True)

    @api.depends('offer_ids')
    def _compute_offer_recieved(self):
        for record in self:
            record.offer_recieved = bool(record.offer_ids)
    
    # @api.depends('offer_recieved')
    # def _compute_offer_state(self):
    #     if self.offer_recieved:
    #         self.state = 'offered_rec'