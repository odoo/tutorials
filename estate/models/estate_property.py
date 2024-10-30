from odoo import fields, models, api
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):

    _name = "estate.property"
    _description = "Estate Property Model"
    _order = "id desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # fields
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, string="Available From", default=lambda self: datetime.today() + timedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Direction',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Direction selection from North,South,East,West",
        )
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        string='State',
        copy=False,
        default='new',
        selection=[('new', 'New'), ('offer received', 'Offer Recieved'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        help="Direction selection from North,South,East,West",
        tracking=True)
    property_type_id = fields.Many2one(
        'estate.property.type',
        string='Property Type',
    )
    salesperson = fields.Many2one(
        'res.users',
        string='Salesman',

    )
    buyer = fields.Many2one(
        'res.partner',
        string='Buyer',
        copy=False
    )
    tag_ids = fields.Many2many(
        'estate.property.tags',
        string="Tags"
    )
    offer_ids = fields.One2many(
        'estate.property.offers',
        "property_id",
    )
    total_area = fields.Float(compute="_compute_area", string="Total Area (sqm)")

    best_price = fields.Float(compute="_compute_best_price", store=True)

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)

    image = fields.Image(string="Property Image", attachment=True)

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'A property expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'A property selling price must be positive'),
    ]

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < (0.9 * record.expected_price) and (record.selling_price > 0):
                raise ValidationError("Selling price cannot be lower than 90 percentage of the expected price.")

    # Methods
    @api.depends('living_area', 'garden_area')
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    @api.onchange('garden_area', 'garden_orientation', 'garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = False

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("You cannot mark a sold property as canceled.")
            record.state = 'canceled'

    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("You cannot mark a canceled property as sold.")
            record.state = 'sold'

    @api.ondelete(at_uninstall=False)
    def unlink_property(self):
        if any(record.state not in ('new', 'canceled') for record in self):
            raise UserError('You cannot delete the records that are not in the "new" or "canceled" state.')
