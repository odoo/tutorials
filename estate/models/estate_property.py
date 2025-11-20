from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate description"

    name = fields.Char(required=True)
    tag_ids = fields.Many2many("estate.property.tag")
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    user_id = fields.Many2one('res.users', string='Salesman', index=True, default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', index=True)
    offer_ids = fields.One2many(
        'estate.property.offer', inverse_name='property_id', string="Offers"
    )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=3),
        string="Available from",
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    total_area = fields.Integer(compute="_compute_total_area")
    garden_area = fields.Integer()
    best_price = fields.Float(compute="_compute_best_price")
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('west', 'West'),
            ('east', 'East')
        ])
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="Estate status",
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        help='This field explain the estate status.',
        required=True,
        copy=False,
        default='new',
    )

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)', 'The expected price must be strictly positive'
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)', 'The selling price must be positive'
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if len(record.offer_ids) > 0:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0

    @api.onchange('garden')
    def _inverse_garden(self):
        for record in self:
            if record.garden:
                record.garden_orientation = 'north'
                record.garden_area = 10
            else:
                record.garden_orientation = ''
                record.garden_area = 0

    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("Canceled property can't be sold.")
            else:
                record.state = "sold"
                return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold property can't be canceled.")
            else:
                record.state = "canceled"
                return True

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if float_compare( record.selling_price, record.expected_price * 0.9, precision_digits=4) == -1 \
                    and (self.state == "offer_accepted"):
                raise ValidationError(
                    "The selling price cannot be lower than 90% of the expected price."
                )
