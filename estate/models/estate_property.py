from dateutil.relativedelta import relativedelta
from datetime import date

from odoo import models, fields, api, exceptions, _
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Integer()
    date_availability = fields.Date(
        default=lambda self: date.today() + relativedelta(months=3),
        copy=False
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(
        readonly=True,
        copy=False
    )
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
    selection=[
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ],
    required=True,
    copy=False,
    default='new',
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
    )
    salesperson_id = fields.Many2one(
        "res.users",
        default=lambda self: self.env.user,
    )
    buyer_id = fields.Many2one(
        "res.partner",
        copy=False,
    )
    tag_ids = fields.Many2many(
        "estate.property.tag",
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
    )
    total_area = fields.Float(
        compute="_compute_total_area"
    )
    best_price = fields.Float(
        compute="_compute_best_price",
    )
    _expected_price = models.Constraint(
        'CHECK(expected_price >= 0)',
        'The expected price must be positive.',
    )
    _selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price must be positive.',
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            record.best_price = max(prices) if prices else 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_cancel_property(self):
        if self.filtered(lambda rec: rec.state == "sold"):
            raise exceptions.UserError(_("Sold properties cannot be cancelled."))
        self.write({"state": "cancelled"})
        return True

    def action_set_sold(self):
        for rec in self:
            if rec.state == "cancelled":
                raise exceptions.UserError(_("Canceled properties cannot be sold."))
            else:
                rec.state = "sold"
        return True

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for rec in self:
            if rec.selling_price == 0:
                return False
            if float_compare(rec.selling_price, rec.expected_price * 0.9, precision_digits=2) < 0:
                raise exceptions.ValidationError(_(
                    "The selling price must be at least 90% of the expected price!\n"
                    "You must reduce the expected price if you want to accept this offer."
                ))

    @api.ondelete(at_uninstall=False)
    def _check_property_deletion(self):
        for rec in self:
            if rec.state not in ("new", "cancelled"):
                raise exceptions.UserError(_(
                    "You can only delete properties in New or Cancelled state."
                ))
