from odoo import models, fields, api, exceptions
from odoo.tools import float_utils # type: ignore
from datetime import date
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Comprehensive platform for managing properties, sales, rentals, and client relationships throughout their entire lifecycle."
    _sql_constraints = [
        ('check_expected_price_positive', 'CHECK (expected_price > 0)', 'Expected price must be positive.'),
        ('check_selling_price_positive', 'CHECK (selling_price >= 0)', 'Selling price must be positive.')
    ]
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price !=0 and float_utils.float_compare(
                record.selling_price,
                record.expected_price * 0.9,
                precision_digits=2
            ) < 0:
                raise exceptions.ValidationError("Selling price must be greater than or equal to 90% of expected price.")
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    
    garden = fields.Boolean()
    @api.onchange("garden")
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = False
    
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('n', 'North'), 
                   ('s', 'South'), 
                   ('e', 'East'), 
                   ('w', 'West')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='Status',
        selection=[('new', 'New'), 
                   ('offer_received', 'Offer Received'), 
                   ('offer_accepted', 'Offer Accepted'), 
                   ('sold', 'Sold'), 
                   ('cancelled', 'Cancelled')],
        default='new',
        required=True,
        copy=False
    )

    buyer_id = fields.Many2one('res.partner', string='Buyer', index=True, copy=False)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', index=True, default=lambda self: self.env.user)

    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    type_id = fields.Many2one('estate.property.type', string='Property Type')

    total_area = fields.Float(
        compute='_compute_total_area',
        string='Total Area'
    )
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area if record.garden_area else record.living_area

    best_price = fields.Float(
        compute='_compute_best_price',
        string='Best Price',
        readonly=True
    )
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0.0)

    def action_sold_property(self):
        for record in self:
            if record.state == 'cancelled':
                raise exceptions.UserError("Cannot set as sold if cancelled")
            record.state = 'sold'
        return True

    def action_cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError("Cannot cancel if already sold")
            record.state = 'cancelled'
        return True

    @api.ondelete(at_uninstall=False)
    def _unlink_if_user_new_cancelled(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise exceptions.UserError("Can't delete an active property!")
