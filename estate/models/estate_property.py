from odoo import models, fields, api
from datetime import timedelta, date
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = 'id desc'

    name = fields.Char(required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(copy=False, default=lambda self: date.today() + timedelta(days=90))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price")
    bedrooms = fields.Integer(default=2)
    active = fields.Boolean(default=True)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage Available")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West")
        ]
    )
    state = fields.Selection(selection=[
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ], default='new', string="Status", copy=False)    
    property_type_id = fields.Many2one('estate.property.type', string="Property Type",
    options={'no_create': True, 'no_edit': True}) 
    buyer_id = fields.Many2one('res.partner', string="Buyer",copy=False)
    seller_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user,required=False)
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string="Status")
    partner_id = fields.Many2one('res.partner', string="Partner", ondelete='restrict')
    price = fields.Float(string="Price")
    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_total_area", store=True,copy=False)
    best_offers = fields.Float(string="Best Offers")
    offer_ids = fields.One2many(
        'estate.property.offer', 
        'property_id', 
        string="Offers"
    )
    validity = fields.Integer(string="Validity (days)")
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True)
    tag_ids = fields.Many2many(
        'estate.property.tag',
        string='Tags'
    )
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    best_price = fields.Float(string="Best Price", compute="_compute_best_price", store=True)
    offer_received = fields.Boolean(string="Offer Received", compute="_compute_offer_received", store=True)
    offer_accepted = fields.Boolean(string="Offer Accepted", compute="_compute_offer_accepted", store=True)
    user_id = fields.Many2one('res.users', string="Salesperson")
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )


    
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False
    
    def action_cancel(self):
        self.state = 'canceled'  
        for record in self:
            if record.state == 'sold':
                raise UserError("A sold property cannot be cancelled.")
            record.state = 'cancelled'

    def action_sold(self):
        self.state = 'sold'
        for record in self:
            if record.state == 'cancelled':
                raise UserError("A cancelled property cannot be sold.")
            record.state = 'sold'
    
    _sql_constraints = [
        ('expected_price_positive', 'CHECK(expected_price > 0)',
         'The expected price must be strictly positive.'),
        ('selling_price_positive', 'CHECK(selling_price >= 0)',
         'The selling price must be positive.')
    ]

    @api.constrains('expected_price')
    def _check_expected_price(self):
     for record in self:
        if record.expected_price <= 0:
            raise ValidationError("The expected price must be strictly positive.")
   

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)
     
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_rounding=0.01):
                continue
            min_price = record.expected_price * 0.9
            # if float_compare(record.selling_price, min_price, precision_rounding=0.01) < 0:
            #     raise ValidationError(
            #         "The selling price cannot be lower than 90% of the expected price."
            #     )
   
    @api.depends('state')
    def _compute_offer_received(self):
        for record in self:
            record.offer_received = record.state == 'offer_received'

    @api.depends('state')
    def _compute_offer_accepted(self):
        for record in self:
            record.offer_accepted = record.state == 'offer_accepted' 

    @api.ondelete(at_uninstall=False)
    def _check_state_on_delete(self):
        for record in self:
            if record.state not in ('new', 'cancelled'):
                raise UserError(
                    "You cannot delete a property unless it is in 'New' or 'Cancelled' state."
                )
                            
    # def action_helper_message(self):
    #     # Logic to determine when to show the helper
    #     if not self.search([]):
    #         return {
    #             'type': 'ir.actions.client',
    #             'tag': 'display_notification',
    #             'params': {
    #                 'title': 'No Properties Found',
    #                 'message': 'Click the button to create your first property.',
    #                 'type': 'warning',
    #             }
    #         }    