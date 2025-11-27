from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc "
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    create_date = fields.Datetime()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        required=True,
        copy=False,
        default="new"
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one("res.users", string="Salesperson")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total_area", string="Total Area", store=True)
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer", store=True)
    validity_days = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    _check_price = models.Constraint(
        'CHECK(expected_price > 0 AND selling_price >= 0)',
        'The Price of a property must be strictly positive.',
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)

    @api.depends("offer_ids.price", "state")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price")) if record.offer_ids else 0.0

    @api.depends("create_date", "validity_days")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            if hasattr(create_date, "date"):
                create_date = create_date.date()
            record.date_deadline = create_date + timedelta(days=record.validity_days)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            if hasattr(create_date, "date"):
                create_date = create_date.date()
            delta = (record.date_deadline - create_date).days if record.date_deadline else 0
            record.validity_days = delta

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                if float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) < 0:
                    raise ValidationError("The selling price cannot be lower than 90% of the expected price.")

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.model
    def create(self, vals):
        record = super().create(vals)
        if record.offer_ids:
            record.state = 'offer_received'
        return record

    def write(self, vals):
        res = super().write(vals)
        if 'offer_ids' in vals:
            for record in self:
                if record.offer_ids and record.state != 'offer_received':
                    record.state = 'offer_received'
        return res

    def action_set_sold(self):
        for record in self:
            if record.state != 'canceled':
                record.state = 'sold'
            else:
                raise UserError("once sold cannot be canceled")

    def action_set_canceled(self):
        for record in self:
            record.state = "canceled"

    def action_back_to_new(self):
        for record in self:
            record.state = "new"

    def _unlink(self):
        for record in self:
            if record.state in ["new"]:
                raise ValidationError("You cannot delete a new or canceled property.")
        return super().unlink()
