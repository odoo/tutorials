from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Property Data Table"
    _inherit = ['mail.thread']
    _order = 'id desc'
    _sql_constraints = [
        (
            'check_expected_price_positive',
            'CHECK(expected_price > 0)',
            'The expected price must be strictly positive.',
        ),
        (
            'check_selling_price_positive',
            'CHECK(selling_price >= 0)',
            'The selling price must be positive.',
        ),
    ]

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    # Default availability date is set to 3 months from today
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: date.today() + relativedelta(months=3),
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", copy=False, readonly=True)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garage_area = fields.Integer(string="Garage Area (sqm)")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ]
    )
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        required=True,
        copy=False,
        default='new',
        group_expand=True,
        tracking=True,
    )
    property_type_id = fields.Many2one(
        'estate.property.type',
        string="Property Type",
        default=lambda self: self.env.ref('estate.property_type_house'),
    )
    salesperson_id = fields.Many2one(
        'res.users', string="Salesman", index=True, default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one('res.partner', string="Buyer", index=True, copy=False, readonly=True)
    tag_ids = fields.Many2many('estate.property.tag', string="Property Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    total_area = fields.Float(compute='_compute_area', string="Total Area (sqm)")
    outside_area = fields.Float(compute='_compute_area', string="Outside Area (sqm)")
    best_price = fields.Float(compute='_compute_best_price', string="Best Offer")
    company_id = fields.Many2one(
        'res.company',
        string="Company",
        required=True,
        default=lambda self: self.env.company
    )
    image = fields.Image(string="Property Image", max_width=256, max_height=256)

    @api.depends('living_area', 'garden_area', 'garage_area')
    def _compute_area(self):
        for record in self:
            record.total_area = sum(
                [record.living_area, record.garden_area, record.garage_area]
            )
            record.outside_area = record.garden_area + record.garage_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    # Constraint to ensure the selling price is at least 90% of the expected price
    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:
            if (
                not float_is_zero(record.selling_price, precision_digits=2) 
                and float_compare(record.selling_price, 0.9 * record.expected_price,
                precision_digits=2) < 0
            ):
                raise ValidationError("Selling price cannot be lower than 90% of the expected price.")

    @api.onchange('garden')
    def _onchange_garden(self):
        self.write(
            {
                'garden_area': 10 if self.garden else 0,
                'garden_orientation': 'north' if self.garden else False,
            }
        )

    @api.onchange('garage')
    def _onchange_garage(self):
        self.write({'garage_area': 0})

    @api.ondelete(at_uninstall=False)
    def prevent_deletion(self):
        if any(record.state not in ['new', 'cancelled'] for record in self):
            raise UserError("Only New or Cancelled properties can be deleted")

    def action_sold(self):
        self.ensure_one()
        for record in self:
            if not record.buyer_id:
                raise UserError("Property does not have any buyer.")
            elif record.state == 'cancelled':
                raise UserError("Cancelled property cannot be sold.")
            elif record.state == 'sold':
                raise UserError("Property is already sold.")
            record.state = 'sold'

    def action_cancel(self):
        self.ensure_one()
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold property cannot be cancelled.")
            elif record.state == 'cancelled':
                raise UserError("Property is already cancelled.")
            record.state = 'cancelled'
