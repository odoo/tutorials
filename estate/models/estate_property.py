from odoo import models, fields, api
from odoo.tools import float_compare, float_is_zero
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    notes = fields.Html()
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: fields.Date.add(fields.Date.today(), months=3)
    )

    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False)
    best_offer = fields.Float(copy=False, compute="_compute_best_offer")

    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    total_area = fields.Integer(
        compute="_compute_total_area",
        store=True,
        string="Total Area (sqm)",
    )
    facades = fields.Integer()
    garage = fields.Boolean()

    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ]
    )

    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('received', 'Offer Received'),
            ('accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        default="new"
    )

    # relations
    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one("res.partner")
    salesman_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max((offer.price for offer in record.offer_ids), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"

    def action_set_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError('A canceled property cannot be sold')
            else:
                record.state = 'sold'
        return True

    def action_set_canceled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('A sold property cannot be canceled')
            else:
                record.state = 'canceled'
        return True

    _check_expected_price = models.Constraint(
        'CHECK(expected_price >= 0)',
        'The expected price of the property should be strictly postitive',
    )

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.state in ("new", "received"):
                return

            if float_compare(record.selling_price, (record.expected_price * 0.9), 2) < 0:
                raise ValidationError("The selling price cannot be lower than 90%% of the expected price")

            if float_is_zero(record.selling_price, 2):
                raise ValidationError("The selling price should be positive")

    @api.ondelete
    def _unlink_property(self):
        if self.state not in ('new', 'canceled'):
            raise UserError("This property can't be deleted")

        return super().unlink()
