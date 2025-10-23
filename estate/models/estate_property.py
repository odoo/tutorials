from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.date_utils import add
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate propreties"
    _order = "id desc"

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'Expected price must be strictly positive.',
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'Selling price must be positive.',
    )
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda x: add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Float()
    garden_orientation = fields.Selection(selection=[('north', 'North'), ('south', 'South'), ('west', 'West'), ('east', 'East')])
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[('new', 'New'), ('received', 'Offer Received'), ('accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        default='new', copy=False, required=True)
    seller_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', readonly=True)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    type_id = fields.Many2one('estate.property.type', string="Type")
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Float(compute="_compute_total_area", readonly=True, copy=False)
    best_price = fields.Float(compute="_get_best_price", readonly=True, copy=False)

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _get_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        self.ensure_one()
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_set_sold(self):
        self.ensure_one()
        if self.state == 'cancelled':
            raise UserError("Cancelled property cannot be set as sold")
        self.state = 'sold'
        return 1

    def action_set_cancelled(self):
        self.ensure_one()
        if self.state == 'sold':
            raise UserError("Sold property cannot be cancelled")
        self.state = 'cancelled'
        return 1

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        self.ensure_one()
        if self.buyer_id and float_compare(self.expected_price, 0.9 * self.selling_price, 0) > 0:
            raise ValidationError("The selling price cannot be lower than 90% of the expected price.")

    @api.ondelete(at_uninstall=False)
    def _unlink_if_not_new_or_cancelled(self):
        if any(record.state in ['new', 'cancelled'] for record in self):
            raise UserError("Can't delete a property which has a state of new or cancelled!")
