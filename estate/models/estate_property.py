from odoo import _, api, exceptions, fields, models
from odoo.tools.date_utils import add
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _order = 'id desc'
    _sql_constraints = [
        ('check_expected_price_strictly_positive', 'CHECK(expected_price > 0)',
         'The expected price of a property should be strictly positive.'),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)',
         'The selling price of a property should be positive or zero.'),
    ]

    name = fields.Char("Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date("Available From", copy=False,
                                    default=lambda _: add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[('north', 'North'),
                   ('south', 'South'),
                   ('east', 'East'),
                   ('west', 'West')],
        help="Orientation of the garden, if it exists.",
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="Status",
        selection=[('new', 'New'),
                   ('offer_received', 'Offer Received'),
                   ('offer_accepted', 'Offer Accepted'),
                   ('sold', 'Sold'),
                   ('cancelled', 'Cancelled')],
        default='new',
        help="State of the property.",
        copy=False,
        required=True,
    )
    property_type_id = fields.Many2one(
        comodel_name='estate.property.type',
        help="Type of the property.",
    )
    buyer_id = fields.Many2one(
        comodel_name='res.partner',
        copy=False,
        help="Buyer of the property.",
    )
    salesperson_id = fields.Many2one(
        comodel_name='res.users',
        default=lambda self: self.env.user,
        help="Salesperson responsible for the property.",
    )
    tag_ids = fields.Many2many(
        string="Tags",
        comodel_name='estate.property.tag',
        help="Tags associated with the property.",
    )
    offer_ids = fields.One2many(
        string="Offers",
        comodel_name='estate.property.offer',
        inverse_name='property_id',
        help="Offers made on the property.",
    )
    total_area = fields.Integer(
        string="Total Area (sqm)",
        compute='_compute_total_area',
        help="Total area of the property, including living area and garden area.",
    )
    best_offer = fields.Float(
        compute='_compute_best_offer',
        help="Best offer made on the property.",
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for property in self:
            property.best_offer = max(property.offer_ids.mapped('price'), default=0.0)

    @api.constrains('expected_price', 'selling_price')
    def _check_prices(self):
        for property in self:
            if (
                    not float_is_zero(property.selling_price, precision_rounding=0.01)
                    and float_compare(property.selling_price,
                                      0.9 * property.expected_price, precision_rounding=0.01) < 0):
                raise exceptions.ValidationError(_("The selling price cannot be lower than 90% of the expected price."))

    @api.onchange('garden')
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = False
        else:
            self.garden_area = 10
            self.garden_orientation = 'north'

    @api.ondelete(at_uninstall=False)
    def _delete_except_new_cancelled(self):
        for property in self:
            if property.state not in ['new', 'cancelled']:
                raise exceptions.UserError(_("You can only delete properties that are new or cancelled."))

    def action_sold(self):
        for property in self:
            if property.state != 'offer_accepted':
                raise exceptions.UserError(_("Only properties with an accepted offer can be sold."))
            property.state = 'sold'
        return True

    def action_cancel(self):
        for property in self:
            if property.state == 'sold':
                raise exceptions.UserError(_("Sold properties cannot be cancelled."))
            property.state = 'cancelled'
        return True
