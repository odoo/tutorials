from odoo import _, api, fields, models
from datetime import timedelta

from odoo.exceptions import UserError


class RealEstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=(lambda x: fields.Date.today() + timedelta(days=90))
    )
    expected_price = fields.Float(required=True, readonly=False)
    selling_price = fields.Float(copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area (sqm)")
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        default="new",
        required=True,
        copy=False,
    )
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")]
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offers_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_area", string="Total Area (sqm)")
    best_offer = fields.Float(compute="_compute_offer", string="Best Offer (EUR)")

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "The expected price of a property should be strictly positive.",
    )

    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)",
        "The selling price of a property should be positive.",
    )

    @api.depends("living_area", "garden_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offers_ids.price")
    def _compute_offer(self):
        for record in self:
            record.best_offer = (
                max(record.offers_ids.mapped("price")) if record.offers_ids else 0
            )

    @api.depends("offers_ids")
    def _compute_state(self):
        for record in self:
            record.state = "offer_received" if record.offer_ids else "new"

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def sold_property(self):
        for record in self:
            if record.state in ["canceled", "new"]:
                raise UserError(
                    _("Only properties with an accepted offer can be sold.")
                )
            record.state = "sold"

    def cancel_property(self):
        for record in self:
            if record.state == "sold":
                raise UserError(_("Sold properties cannot be canceled."))
            record.state = "canceled"

    @api.ondelete(at_uninstall=False)
    def delete(self):
        for record in self:
            if record.state not in ["new", "canceled"]:
                raise UserError(_("Only new or canceled properties can be deleted."))
