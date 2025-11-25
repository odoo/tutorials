#!/usr/bin/env python3
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

from odoo import api, models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_avaliability = fields.Date(
        copy=False, default=fields.Date.today() + relativedelta(month=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Orientation",
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    customer = fields.Many2one("res.partner", string="Customer", copy=False)
    salesperson = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offer")
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Integer(compute="_compute_best_price")

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "A property expected price must be strictly positive.",
    )
    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)", "A property selling price must be positive."
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if not record.mapped("offer_ids.price"):
                record.best_price = 0
            else:
                record.best_price = max(record.mapped("offer_ids.price"))

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_sold_property(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled Property cannot be Sold")
            else:
                record.state = "sold"
        return True

    def action_cancel_offer(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold Property cannot be Cancelled")
            else:
                record.state = "cancelled"
        return True

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price_persentage(self):
        for record in self:
            selling_price_persentage = (
                record.selling_price / record.expected_price
            ) * 100
            if selling_price_persentage >= 90 or selling_price_persentage == 0:
                pass
            else:
                raise ValidationError(
                    "the selling price cannot be lower than 90% of the expected price."
                )

    @api.ondelete(at_uninstall=False)
    def _unlink_prevent_property_on_state(self):
        for record in self:
            if record.state not in ("new", "cancelled"):
                raise UserError(
                    "Can Delete property only on 'New' or 'Cancelled' state!"
                )
