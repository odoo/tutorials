from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_is_zero, float_compare


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate property model"
    _order = "id desc"

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price of a property must be positive.'
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price > 0)',
        'The selling price of a property must be positive.'
    )

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False, readonly=True)
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
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        help="Orientation is used to define the orientation of the garden"
    )
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        string='State',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        required=True,
        default="new"
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Types")
    salesman = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', string='Buyer')
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute="_compute_area", string="Total Area (sqm)")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    @api.depends('living_area', 'garden_area')
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_partner_id(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_set_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties cannot be canceled")
            else:
                record.state = "canceled"
        return True

    def action_set_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("Canceled properties cannot be sold")
            else:
                record.state = "sold"
        return True

    @api.constrains('selling_price')
    def check_selling_price(self):
        for record in self:
            if (
                not float_is_zero(record.selling_price, 2)
                and (float_compare(record.selling_price, (record.expected_price * 0.90), 2) < 0)
            ):
                raise ValidationError("The selling price cannot be below 90 pourcent of the expected price.")

    @api.ondelete(at_uninstall=True)
    def _delete_property(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise UserError("You can't delete this property because this state is %(value)s." % {'value': record.state})
