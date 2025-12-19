from datetime import datetime

from dateutil.relativedelta import relativedelta
from odoo import api, exceptions, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property data model"

    name = fields.Char(required=True)
    description = fields.Text()
    active = fields.Boolean(default=True)
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=datetime.now() + relativedelta(month=3)
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
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="Indicates the direction the garden is facing with respect to the house",
    )
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
        help="State of the proprty listing lifecycle",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = (
                max(record.offer_ids.mapped("price")) if record.offer_ids else 0
            )

    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = "north" if self.garden else None

    def sold_estate_property(self):
        for record in self:
            if record.state != "cancelled":
                record.state = "sold"
            else:
                raise exceptions.UserError("can't sell a cancelled property")

    def cancel_estate_property(self):
        for record in self:
            if record.state != "sold":
                record.state = "cancelled"
            else:
                raise exceptions.UserError("can't cancel a sold property")

    def reject_other_offers(self, winning_offer):
        for record in self:
            for offer in record.offer_ids:
                if offer != winning_offer:
                    offer.status = "refused"
