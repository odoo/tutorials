from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, exceptions
from odoo.tools import float_is_zero, float_compare


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _order = 'id desc'

    name = fields.Char('Title', required=True, translate=True)
    description = fields.Text('Description', translate=True)
    postcode = fields.Char('Postcode')
    date_availability = fields.Date(
        string='Available From',
        default=lambda _: fields.Date.today() + relativedelta(months=3),
        copy=False
    )
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('Selling price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage', default=False)
    garden = fields.Boolean('Garden', default=False)
    garden_area = fields.Integer('Garden area (sqm)')
    garden_orientation = fields.Selection(
        string='Garden orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help='Garden orientation is important for determining how much sunlight and warmth the outdoor space receives'
    )
    active = fields.Boolean('Active', default=False)
    status = fields.Selection(
        string='Status',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        default='new',
        required=True,
    )
    property_type_id = fields.Many2one("estate.property.type", string='Type')
    property_tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    property_offer_ids = fields.One2many('estate.property.offer', inverse_name="property_id", string='Offers', copy=False)
    # Computed Field
    total_area = fields.Integer('Total area (sqm)', compute='_compute_total_area', readonly=True, copy=False)
    best_price = fields.Float('Best offer', compute='_compute_best_price', readonly=True, copy=False)
    # Other Info
    salesperson_id = fields.Many2one(
        comodel_name='res.users',
        string='Salesman',
        default=lambda self: self.env.user)
    buyer_id = fields.Many2one(
        comodel_name='res.partner',
        string='Buyer',
        copy=False,
        readonly=True,
    )

    _check_expected_price = models.Constraint(
        'check(expected_price > 0)',
        'The expected price must be a positive amount and cannot be zero!',
    )
    _check_selling_price = models.Constraint(
        'check(selling_price >= 0)',
        'The selling price must be a positive amount!',
    )

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        if any(not record.status in ['new', 'cancelled'] for record in self):
            raise exceptions.UserError(f"Can't delete property with status different from NEW or CANCELLED.")

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:

            if float_is_zero(value=record.selling_price, precision_digits=2):
                # no accepted offers yet
                return

            bottom_bound = .9 * record.expected_price
            if float_compare(record.selling_price, bottom_bound, precision_digits=2) < 0:
                raise exceptions.ValidationError("The selling price cannot be lower than 90% of the expected price.")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("property_offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.property_offer_ids:
                record.best_price = max(record.property_offer_ids.mapped('price'))
            else:
                record.best_price = 0

    @api.onchange('garden')
    def _onchange_garden_flag(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
            return

        self.garden_area = None
        self.garden_orientation = None

    def ensure_status_is_not(self, statuses, error_message=None):
        """ Ensures that the status is not equal or included in statuses """
        if not statuses:
            return

        if isinstance(statuses, str):
            statuses = [statuses]

        if not isinstance(statuses, (list, tuple, set)):
            raise TypeError('statuses must be a string, list, tuple, or set')

        if self.status in statuses:
            msg = error_message or f'Action not allowed for status: {self.status}'
            raise exceptions.UserError(msg)

    def ensure_no_accepted_offers(self, error_message=None):
        if not self.property_offer_ids:
            return

        if "accepted" in self.property_offer_ids.mapped("status"):
            msg = error_message or 'Action not allowed'
            raise exceptions.UserError(msg)

    # ACTIONS

    def action_set_status_cancelled(self):
        for record in self:
            record.ensure_status_is_not("sold", error_message="You cannot cancel a sold property")
            record.status = "cancelled"

        return True

    def action_set_status_sold(self):
        for record in self:
            record.ensure_status_is_not("cancelled", error_message="You cannot sell a cancelled property")
            record.status = "sold"

        return True
