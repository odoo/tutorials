from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, exceptions, fields, models


class RealEstate(models.Model):
    _name = 'estate.property'
    _description = 'RealEstate Model'
    _order = 'id DESC'
    _inherit = ['mail.thread']

    #--------------------------
        #Default Methods
    #--------------------------

    def _default_date_availibility(self):
        today = datetime.today()
        default_date = today + relativedelta(months=3)
        return default_date.date()


    name = fields.Char(required=True,string="Name")
    property_type_id = fields.Many2one(comodel_name='estate.property.type', string="Propery Type")
    buyer_id = fields.Many2one(comodel_name='res.partner', string="Buyer", copy=False)
    salesperson_id = fields.Many2one(comodel_name='res.users', string="Seles Person",
        default=lambda self: self.env.uid)
    tag_ids = fields.Many2many(comodel_name='estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availibility = fields.Date(
        string="Date Avalibility",
        default=lambda self: self._default_date_availibility(),
        copy=False)
    expected_price = fields.Float(required=True, string="Expected Price")
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bed Rooms", default=2, copy=False)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        selection=[
            ('north', "North"),
            ('east', "East" ),
            ('west', "West"),
            ('south', "South")
        ],
        default = 'north',
        string = "Garden Orientation"
    )
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer_Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        string = 'State',
        default = "new",
        group_expand=True
    )
    total_area = fields.Float(string="Total Area", compute='_compute_total_area')
    best_price = fields.Float(string="Best Price", compute='_compute_best_price')
    image = fields.Image(readonly=False, store=True)
    company_id = fields.Many2one('res.company', string="Company", 
        default=lambda self: self.env.company)

    #--------------------------------
        #Compute Methods
    #--------------------------------

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for records in self:
            records.total_area = records.living_area + records.garden_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0.0)

    #--------------------------
        #Onchange and Constraint Method
    #--------------------------

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.write({'garden_area' : 10, 'garden_orientation' : 'north'})
        else:
            self.write({'garden_area' : 0, 'garden_orientation' : ''})

    @api.constrains('expected_price', 'selling_price')
    def _check_price(self):
        for record in self:
            if record.expected_price <= 0:
                raise exceptions.ValidationError("Expected Price must be positive")
            if record.selling_price < record.expected_price * 0.9 :
                raise exceptions.ValidationError("Selling Price must be more then or equal to 90'%' of expected price")

    #-----------------------------------
        #CRUD Methods
    #----------------------------------

    @api.ondelete(at_uninstall=False)
    def _check_state(self):
        for record in self:
            if (record.state != 'new' and record.state != 'cancelled'):
                raise exceptions.ValidationError("Only New and Cancelled Property can be deleted")

    #------------------------------------
        #Action Methods
    #-----------------------------------

    def action_sold(self):
        if not self.buyer_id:
            raise exceptions.UserError("This Property dose not have any buyer")
        if self.state == 'sold':
            raise exceptions.UserError("This property is already sold")
        elif self.state == 'cancelled':
            raise exceptions.UserError("Cancelled Property cannot be sold")
        self.state = 'sold'

    def action_cancelled(self):
        if self.state == 'cancelled':
            raise exceptions.UserError("This Property is already Cancelled")
        if self.state == 'sold':
            raise exceptions.UserError("Sold Property cannot be cancelled")
        self.state = 'cancelled'
