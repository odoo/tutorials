from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
from odoo.tools.float_utils import float_compare,float_is_zero
from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate property used to buy and sell houses"

    _positive_price = models.Constraint('CHECK (expected_price>=0)',
                    'Expected price must be positive',
                    )
    _selling_price = models.Constraint('CHECK(selling_price>=0)',
    'Selling price must be positive')

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=lambda self: fields.Date.context_today(self) + relativedelta(months=3),
        copy=False,
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(
        default=2,
    )
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(required=True)
    garden_orientation = fields.Selection(
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )

    state = fields.Selection(
        selection=[
            ("New", "New"),
            ("Offer Accepted", "Offer Accepted"),
            ("Offer Received", "Offer Received"),
            ("Sold", "Sold"),
            ("Cancelled", "Cancelled"),
        ],
    )
    status = fields.Selection(
        selection=[
            ('new', "New"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
            ('reset', "reset"),
        ],
        string="Status",
        default='new',
    )

    active = fields.Boolean(default=True)

    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
    )

    salesman_id = fields.Many2one(
        'res.users',
        string="Salesman",
        default=lambda self: self.env.user,
    )

    buyer_id = fields.Many2one(
        'res.partner',
        string="Buyer",
        copy=False,
    )

    tag_ids = fields.Many2many(
        string="Tags",
        comodel_name='estate.property.tag',
    )

    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string='Offers',
        )

    total_area = fields.Float(
        compute="_compute_total_area",
        string='Total Area',
        store=True,
        help="Auto Computed field",
        )
    best_price = fields.Integer(string="Best Price", compute="_compute_best_price")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for rec in self:
            if rec.offer_ids:
                rec.best_price = max(rec.offer_ids.mapped("price"))
            else:
                rec.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def sold(self):
        for rec in self:
            if rec.status == 'cancelled':
                message = "Property already cancelled"
                raise UserError(message)
            if rec.status == 'sold':
                message = "Already sold cannot be sold again"
            rec.status = 'sold'

    def cancel(self):
        for rec in self:
            if rec.status == 'sold':
                message = "Cannot be cancelled as its already sold"
                raise UserError(message)
            if rec.status == 'cancelled':
                message = "Already cancelled cannot be cancelled again"
            rec.status = 'cancelled'

    def reset(self):
        for rec in self:
            if rec.status == 'sold' or rec.status == 'cancelled':
                rec.status = 'new'
            else:
                message = "Only for sold and cancelled items "
                raise UserError(message)
    
    @api.constrains('selling_price')
    def selling_price(self):
        for rec in self:
            if float_is_zero(rec.selling_price,precision_digits=2):
                continue
            min_price=rec.expected_price*0.9
            if float_compare(rec.selling_price,min_price,precision_digits=2)<0:
                message="Price cannot be less than 90%"
                raise ValidationError(message)
