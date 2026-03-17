from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string='Description')

    postcode = fields.Char()
    date_availability = fields.Date(
        string='Available From',
        copy=False,
        default=lambda self: fields.Date.add(fields.Date.today(), days=90)
    )

    expected_price = fields.Float()
    best_price = fields.Float(compute='_compute_best_price', readonly = True, store=True)

    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms', default=0)
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Has garage')


    living_area = fields.Float(string='Living_Area(sqm)')
    garden = fields.Boolean(string='Has garden')
    garden_area = fields.Float(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ],
        string="Garden Orientation",
    )

    total_area = fields.Float(compute='_compute_total_area', readonly = True, store=True)

    last_seen = fields.Datetime(string='Last Seen', default=fields.Datetime.now)
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        string="Status",
    )


    salesman_id = fields.Many2one(comodel_name='res.users', string="Salesman", default =lambda self: self.env.user )
    buyer_id = fields.Many2one(comodel_name='res.partner', string="Buyer", copy=False )
    property_type_id = fields.Many2one(comodel_name='estate.property.type', string="Property Type")
    tag_ids = fields.Many2many(comodel_name='estate.property.tag', string="Tags")
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_id')




    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            record.best_price = max(prices) if prices else 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0 
                record.garden_orientation = ''
    
    def action_sell(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("A canceled property cannot be sold!")
            elif record.state == 'sold':
                 raise UserError("The property is already sold!")

            record.state = 'sold'
        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("A Sold property cannot be canceled!")     
            record.state = 'cancelled'
        return True
