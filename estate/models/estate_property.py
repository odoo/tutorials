from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo import _

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate model"

    name = fields.Char(required=True, default="My new house")
    description = fields.Text(default="when duplicated status and date are not copied")
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: datetime.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ], default='new', copy=False, string='Status')

    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    salesperson_id = fields.Many2one('res.users', string="Salesperson")
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price') + [0])

    # called if garden value get changed
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # action methods (assigned to buttons)
    # error raised if property is canceled
    def action_set_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError(_("A canceled property cannot be set as sold."))
            record.state = 'sold'

    # error raised if property is sold
    def action_set_canceled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_("A sold property cannot be canceled."))
            record.state = 'canceled'

    _sql_constraints = [('strictly_positive_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
                        ('positive_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be strictly positive.'),
    ]
    
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2) and (float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0):
                raise ValidationError(_(r"The selling price cannot be lower than 90% of the expected price"))