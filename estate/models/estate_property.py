from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property for the estate module"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Orientation is used to define the orientation of the garden"
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        help="Current status of the property (New, Offer Received, Offer Accepted, Sold, or Cancelled).",
        default='new',
        required=True,
        copy=False
    )
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", index=True, copy=False)
    salesman_id = fields.Many2one("res.users", string="Salesman", index=True, default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = None

    def action_sell_property(self):
        for record in self:
            if record.state != 'offer_accepted':
                # continue
                raise UserError(self.env._("You cannot sell a cancelled property."))
            record.state = 'sold'
        return True

    def action_cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(self.env._("Can't cancel a sold property."))
            record.state = 'cancelled'
        return True

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'A property expected price must be strictly positive'
    )

    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'A property selling price must be positive'
    )

    @api.constrains('selling_price')
    def _check_ninety_percent_expected_price(self):
        for record in self:
            if (
                not float_is_zero(record.selling_price, precision_digits=2)
                and float_compare(record.expected_price * 0.9, record.selling_price, precision_digits=2) == 1
            ):
                raise ValidationError(self.env._('Selling price must at least be 90% of the expected price'))

    @api.ondelete(at_uninstall=False)
    def _unlink_expect_not_new_or_cancelled(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError(self.env._("Only new and cancelled properties can be deleted."))
