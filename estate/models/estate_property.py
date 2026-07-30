from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Estate Property"
    _order = 'id desc'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=fields.Date.add(fields.Date.today(), months=3),
        copy=False,
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[('north', "North"), ('south', "South"), ('east', "East"), ('west', "West")],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
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
    )
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
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
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')

    total_area = fields.Integer(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_offer')

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        "The expected price must be strictly positive.",
    )

    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        "The selling price must be positive.",
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
                continue

            record.best_price = 0.0

    @api.onchange('garden')
    def _onchange_property(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
            return

        self.garden_area = None
        self.garden_orientation = None

    @api.ondelete(at_uninstall=False)
    def _check_state(self):
        for record in self:
            if record.state not in {'new', 'canceled'}:
                raise UserError(self.env._("Can't delete a property if the state is not New or Cancelled."))

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                if float_compare(
                        record.selling_price,
                        0.9 * record.expected_price,
                        precision_digits=2) < 0:
                    raise ValidationError(
                        self.env._("The selling price should be at least 90% the expected price")
                    )

    def action_cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(self.env._("A sold property cannot be cancelled."))

            record.state = 'cancelled'

        return True

    def action_sold_property(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(self.env._("A cancelled property cannot be sold."))

            record.state = 'sold'

        return True
