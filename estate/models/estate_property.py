from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime
from dateutil.relativedelta import relativedelta


class test_model(models.Model):
    _name = "estate.property"
    _description = "Sample model"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text("description")
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=(datetime.today() + relativedelta(months=3)).date()
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer()

    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ("north", "NORTH"),
            ("south", "SOUTH"),
            ("east", "EAST"),
            ("west", "WEST"),
        ],
    )
    sequence = fields.Integer("Sequence", default=1)
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one("estate.property.type", ondelete="cascade")
    salesman_id = fields.Many2one(
        "res.users", ondelete="restrict", default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", ondelete="restrict", copy=False)
    tag_ids = fields.Many2many("estate.property.tags")
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer", inverse_name="property_id"
    )
    total_area = fields.Integer(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer")
    status = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer received"),
            ("offer_accepted", "Offer accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        default="new",
        copy=False,
    )
    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "Expected price must be strictly positive",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "Selling price must be non-negative",
        ),
    ]

    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_new_canceled(self):
        for record in self:
            if (
                record.status == "offer_received"
                or record.status == "offer_accepted"
                or record.status == "sold"
            ):
                raise UserError("Only new and canceled properties can be deleted")

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            if not record.offer_ids:
                record.best_offer = 0
                continue
            record.best_offer = max(record.offer_ids.mapped("price"))

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        for record in self:
            if (
                record.status == "new"
                or record.status == "offer_accepted"
                or record.status == "offer_received"
            ):
                record.status = "sold"
            elif record.status == "canceled":
                raise UserError("Canceled property can't be sold")
            else:
                raise UserError("Property already sold")

    def action_cancel(self):
        for record in self:
            if (
                record.status == "new"
                or record.status == "offer_accepted"
                or record.status == "offer_received"
            ):
                record.status = "canceled"
            elif record.status == "sold":
                raise UserError("Sold property can't be canceled")
            else:
                raise UserError("Property already canceled")
