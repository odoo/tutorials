from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Handle real estate property"
    _order = "id desc"

    name = fields.Char(string='Title', required=True)
    description = fields.Text()
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Available From', copy=False, default=fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='Status',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'),
                    ('offer_accepted', 'Offer accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        required=True,
        copy=False,
        default='new',
    )

    property_type_id = fields.Many2one('estate.property.type')
    buyer_id = fields.Many2one('res.partner', copy=False)
    salesman_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')

    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(string='Best Offer', compute="_compute_best_price")

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)

    _expected_price_gt_zero = models.Constraint(
        'CHECK(expected_price > 0)', 'A property expected price must be strictly positive',
    )
    _selling_price_gt_zero = models.Constraint(
        'CHECK(selling_price >= 0)', 'A property selling price must be positive',
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped('price'), default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = False
            self.garden_orientation = False

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        precision = 2
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=precision) and float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=precision) < 0:
                raise ValidationError(_('The selling price cannot be lower than 90% of the expected price'))

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise UserError(_("You cannot delete a property that is not new or cancelled."))

    def action_set_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError(_("Canceled properties can't be sold."))
            record.state = 'sold'
        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_("Canceled properties can't be canceled."))
            record.state = 'canceled'
        return True
