#!/usr/bin/env python3

from typing import final
from odoo import models, fields, api, exceptions, tools

@final
class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Test Model Description here"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        "Available From",
        copy=False,
        default=lambda _: fields.Date.add(fields.Datetime.now(), months=3),
    )

    @api.ondelete(at_uninstall=False)
    def _unlink_except_wrong_state(self) -> None:
        record: EstateProperty
        for record in self:
            if record.state in ["new", "cancelled"]:
                raise exceptions.UserError(f"Cannot delete a property of state {record.state}")


    @api.model_create_multi
    def create(self: "EstateProperty", vals_list: list[api.ValuesType]):
        for val in vals_list:
            val["state"] = "received"
        return super().create(vals_list)

    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area (sqm)")
    res_users_id = fields.Many2one("res.users")

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
            ("offer", "Offer"),
            ("received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        copy=False,
        default="new",
        string="State",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        "res.users", string="Sales Person", default=lambda self: self.env.uid
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    estate_property_offer_ids = fields.One2many(
        "estate.property.offer", "estate_property_id"
    )

    total_area = fields.Integer(compute="_compute_total_area")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self) -> None:
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    @api.depends("estate_property_offer_ids.price", "estate_property_offer_ids.status")
    def _compute_best_price(self) -> None:
        record: EstatePropert
        for record in self:
            offers = record.estate_property_offer_ids
            offers = offers.filtered(lambda o: o.status != "refused")
            record.best_price = max(offers.mapped("price") or [0])

    @api.onchange("garden")
    def _onchange_garden(self) -> None:
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = "north" if self.garden else ""

    def action_cancel_property(self) -> bool:
        record: EstateProperty
        for record in self:
            if record.state == "sold":
                raise exceptions.UserError("You can't cancel a sold property")
            record.state = "cancelled"
        return True

    def action_sell_property(self) -> bool:
        record: EstateProperty
        for record in self:
            if record.state == "cancelled":
                raise exceptions.UserError("You can't sell a cancelled property")
            record.state = "sold"
        return True

    _sql_constraints = [
        (
            "positive_expected_price",
            "CHECK(expected_price > 0)",
            "Expected price should be stictly positive",
        ),
        (
            "positive_selling_price",
            "CHECK(selling_price >= 0)",
            "Selling price should be positive",
        ),
    ]

    @api.constrains("selling_price", "expected_price", "state")
    def _check_selling_price(self) -> None:
        record: EstateProperty
        for record in self:
            if record.state != "offer_accepted":
                continue
            is_lower = (
                tools.float_compare(
                    record.selling_price,
                    record.expected_price * 0.9,
                    precision_digits=2,
                )
                == -1
            )
            if is_lower:
                raise exceptions.ValidationError(
                    "Selling price cannot be lower than 90% of the expected price."
                )
