from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import date_utils
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real-estate properties"
    _order = "id desc"

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The expected price must be positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'The selling price must be positive.')
    ]

    name = fields.Char(
        string="Property Reference",
        required=True, copy=False, readonly=False,
        default='New'
    )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date("Available From", copy=False, default=date_utils.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        required=True,
        copy=False,
        default='new',
        readonly=True
    )
    property_type_id = fields.Many2one('estate.property.type')
    buyer_id = fields.Many2one('res.partner', copy=False)
    seller_id = fields.Many2one('res.users', "Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Integer("Total area (sqm)", compute='_compute_total_area')
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for estate_property in self:
            estate_property.total_area = estate_property.living_area + estate_property.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for estate_property in self:
            estate_property.best_price = max(
                estate_property.offer_ids.mapped('price')) if estate_property.offer_ids else None

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for estate_property in self:
            if (
                not float_is_zero(estate_property.selling_price, precision_digits=3) and
                float_compare(estate_property.selling_price, 0.9 * estate_property.expected_price, precision_digits=3) == -1
            ):
                raise ValidationError("The selling price must be at least 90% of the expected price.")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('estate.property')

        return super().create(vals_list)

    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_is_valid(self):
        if any(estate_property.state not in ['new', 'cancelled'] for estate_property in self):
            raise UserError("Cannot delete a property unless it is New or Cancelled.")

    def action_set_sold(self):
        if self.state == 'cancelled':
            raise UserError("A cancelled property cannot be sold.")
        self.state = 'sold'
        return True

    def action_set_cancelled(self):
        if self.state == 'sold':
            raise UserError("A sold property cannot be cancelled.")
        self.state = 'cancelled'
        return True
