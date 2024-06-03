# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Real Estate properties"
    _order = 'id desc'
    _sql_constraints = [
        (
            'positive_expected_price',
            'CHECK(expected_price > 0)',
            "Expected Price must be strictly positive.",
        ),
        ('positive_selling_price', 'CHECK(selling_price >= 0)', "Selling Price must be positive."),
    ]

    company_id = fields.Many2one(
        'res.company',
        required=True,
        default=lambda self: self.env.company.id,
    )
    name = fields.Char("Property Name", required=True)
    description = fields.Text("Description")
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('canceled', "Canceled"),
        ],
        required=True,
        copy=False,
        default='new',
    )
    property_type_id = fields.Many2one('estate.property.type')
    postcode = fields.Char("Post Code")
    date_availability = fields.Date(
        "Available From",
        copy=False,
        default=fields.Datetime.add(fields.Datetime.today(), months=3),
    )
    expected_price = fields.Float("Expected Price", digits="%.2f", required=True)
    selling_price = fields.Float("Selling Price", digits="%.2f", readonly=True, copy=False)
    bedrooms = fields.Integer("Number of Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Number of Facades")
    garage = fields.Boolean("Has Garage")
    garden = fields.Boolean("Has Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ('north', "North"),
            ('east', "East"),
            ('south', "South"),
            ('west', "West"),
        ],
    )
    buyer_id = fields.Many2one('res.partner', readonly=True, copy=False)
    salesperson_id = fields.Many2one(
        'res.users',
        domain=lambda self: [('groups_id', 'in', self.env.ref('base.group_user').id)],
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Float("Total Area (sqm)", compute='_compute_total_area')
    best_price = fields.Float("Best Offer", compute='_compute_best_price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            ratio = record.selling_price / record.expected_price
            if (
                    not float_is_zero(record.selling_price, precision_rounding=0.01)
                    and float_compare(ratio, 0.90, precision_rounding=0.01) < 0
            ):
                raise ValidationError(
                    _(
                        "The selling price must be at least 90% of the expected price. "
                        "To accept this offer, reduce the expected price."
                    )
                )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def delete(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise UserError(_("Only New and Canceled properties can be deleted."))

    def action_sell(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError(_("Canceled properties cannot be sold."))
            if len(record.offer_ids) <= 0:
                raise UserError(_("Cannot mark a property without offer as sold."))
            record.state = 'sold'
        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_("Sold properties cannot be canceled."))
            record.state = 'canceled'
        return True
