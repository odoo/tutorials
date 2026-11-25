from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property"
    # _order = "id desc" # Added a view ordering instead
    _check_expected_price = models.Constraint("CHECK (expected_price > 0)",
                                                "The expected price needs to be strictly positive")
    _check_selling_price = models.Constraint("CHECK (selling_price >= 0)",
                                            "The selling price needs to be positive")

    name = fields.Char(required=True, string='Title')
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Datetime(string='Available From', copy=False,
                                        default=lambda self: fields.Date.context_today(self) + relativedelta(months=3))

    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    best_price = fields.Float(compute="_compute_best_price")
    bedrooms = fields.Integer(default=2)
    facades = fields.Integer()
    living_area = fields.Integer()
    total_area = fields.Integer(compute="_compute_total_area")

    garage = fields.Boolean()
    garden = fields.Boolean(default=False)
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden orientation',
        selection=[('north', 'North'), ('east', 'East'),
                   ('south', 'South'), ('west', 'West')],
        help="Orientation of the garden")

    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one("res.partner", copy=False)
    salesperson_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='Status',
        default='new', required=True, copy=False,
        selection=[('new', 'New'), ('received', 'Offer Received'),
                   ('accepted', 'Offer Accepted'), ('sold', 'Sold'),
                   ('cancelled', 'Cancelled')])

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids", "offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        for record in self:
            if record.state == 'new' or record.state == 'cancelled':
                raise UserError("Can't delete a new or cancelled property!")

    def action_sell_property(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(self.env._("Cancelled properties cannot be sold"))
            if len(list(filter(lambda offer: offer.status == 'accepted',record.offer_ids))) != 1:
                raise UserError(self.env._("Can't sell a property that doesn't have an accepted offer!"))
            record.state = 'sold'
        return True

    def action_cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(self.env._("Sold properties cannot be cancelled"))
            record.state = 'cancelled'
        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_expected_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                if float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) < 0:
                    raise ValidationError("The selling price cannot be less than 90% of the expected_price")
