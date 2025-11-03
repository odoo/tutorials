from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Float(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Float(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
        ]
    )
    active = fields.Boolean(default=False)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ]
    )
    property_type_id = fields.Many2one("estate.property.type")
    buyer = fields.Many2one("res.partner", copy=False)
    salesperson = fields.Many2one("res.users", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer")
    
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            if not record.mapped('offer_ids.price'):
                record.best_offer = 0
            else:
                record.best_offer = max(record.mapped('offer_ids.price'))
    
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("sold property cannot be cancelled.")
            else:
                record.state = 'cancelled'

    def sold_property(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("cancelled property cannot be sold.")
            else:
                record.state = 'sold' 

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price>=0)', 'expected price must be positive'),
        ('check_selling_price', 'CHECK(selling_price>=0)', 'selling price must be positive')
    ]

    @api.constrains('selling_price',  'expected_price', 'state')
    def _check_selling_price(self):
        for record in self:
            if float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) < 0 and (record.state == 'sold' or record.state == 'offer_accepted'):
                raise ValidationError("the selling price is lower")
                