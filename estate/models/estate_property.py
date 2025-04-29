from dateutil.relativedelta import relativedelta

from odoo import _, api, models, fields
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


def _default_date_availability(_):
    return fields.Date.today() + relativedelta(months=3)


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property Information"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    sequence = fields.Integer('Sequence', default=10)
    property_tag_ids = fields.Many2many("estate.property.tag")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type", group_expand="group_by_empty")
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=_default_date_availability
    )
    state = fields.Selection(
        string='Status',
        required=True,
        copy=False,
        default='new',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
    )
    expected_price = fields.Float(required=True)
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Orientation of the garden"
    )
    total_area = fields.Integer(
        string="Total Area (sqm)",
        compute="_compute_total_area",
    )
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    offers_ids = fields.One2many('estate.property.offer', 'property_id')
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive.'),
    ]

    @api.model
    def group_by_empty(self, types, domain):
        return types.search([])  # this is equivalent to return self.env['estate.property.type'].search([])

    def action_set_sold(self):
        for property in self:
            if property.state == 'cancelled':
                raise UserError(_("Canceled properties cannot be set as sold."))
            property.state = 'sold'
        return True

    def action_cancel(self):
        for property in self:
            if property.state == 'sold':
                raise UserError(_("Sold properties cannot be canceled."))
            property.state = 'cancelled'
        return True

    @api.ondelete(at_uninstall=False)
    def _check_unlink_state(self):
        for property in self:
            if property.state not in ('new', 'cancelled'):
                raise UserError(_("You cannot delete a property that is not in 'New' or 'Cancelled' state."))

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for property in self:
            if not float_is_zero(property.expected_price, precision_digits=2):
                accepted_offers = property.offers_ids.filtered(lambda o: o.status == 'accepted')
                if accepted_offers:
                    if float_compare(property.selling_price, property.expected_price * 0.90, precision_digits=2) == -1:
                        raise ValidationError("Selling price cannot be lower than 90 percent of expected price")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends('offers_ids.price')
    def _compute_best_price(self):
        for property in self:
            if property.offers_ids:
                property.best_price = max(property.offers_ids.mapped('price'))
            else:
                property.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False
