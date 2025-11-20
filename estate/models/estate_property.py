from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"
    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price should be stricly positive'
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price should be positive'
    )

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), months=3), string="Available From")
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
        selection=[
                ('north', 'North'),
                ('west', 'West'),
                ('south', 'South'),
                ('east', 'East')
            ],
        help="Choose the appropriate orientation of the garden"
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="Estate status",
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        help='This field explain the estate status.',
        required=True,
        copy=False,
        default='new'
    )
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    seller_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user, domain="[('type', '=', 'internal')]")
    buyer_id = fields.Many2one("res.partner", string="Buyer", domain="[('type', '=', 'portal')]")
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_total_area", string="Total Area (sqm)")
    best_price = fields.Float(compute="_compute_best_offer", string="Best Offer")

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price")) if len(record.offer_ids) > 0 else 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if not record.garden:
                record.garden_area = 0
                record.garden_orientation = ''
            else:
                record.garden_area = 10
                record.garden_orientation = 'north'

    def estate_property_action_sold(self):
        self.__estate_property_action_sold_cancel('sold', "A cancelled property cannot be sold!", "This property is already sold!")

    def estate_property_action_cancel(self):
        self.__estate_property_action_sold_cancel('cancelled', "A sold property cannot be cancelled!", "This property is already cancelled!")

    def __estate_property_action_sold_cancel(self, target, error_message, error_same_target_message):
        for record in self:
            # exclude target from next condition
            if record.state == target:
                raise UserError(error_same_target_message)
            # easiest way to exclude the other state
            elif record.state in ('sold', 'cancelled'):
                raise UserError(error_message)
            # the property can be sold/cancelled
            else:
                record.state = target

    @api.constrains('selling_price')
    def _check_price_constraint(self):
        for record in self:
            if record.selling_price and float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=4) < 0:
                raise ValidationError("The price cannot be les than 90% of the expected price")
            
    @api.onchange("offer_ids")
    def _onchange_offer_ids(self):
        for record in self:
            if len(record.offer_ids) > 0:
                record.state = "offer_received"
            else:
                record.state = "new"
