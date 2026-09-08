from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=lambda self: (
            fields.Date.today() + relativedelta(months=3)
        )
    )
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Integer(compute="_compute_total")
    best_offer = fields.Float(
        string="Best Offer", compute="_compute_best_offer")
    garden_orientation = fields.Selection(
        [
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('booked', "Booked"),
            ('sold', "Sold"),
            ('canceled', "Canceled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False,
    )
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
    )
    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Tags",
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offer",
    )
    issue_ids = fields.One2many(
        "estate.property.maintenance",
        "property_id"
    )
    booking_ids = fields.One2many(
        "estate.property.booking",
        "property_id"
    )
    booking_count = fields.Integer(
        compute="_compute_booking_count",
    )

    _check_expected_price_constraint = models.Constraint(
        "CHECK(expected_price>0)", "Expected price must be strictly positive"
    )

    _check_selling_price_constraint = models.Constraint(
        "CHECK(selling_price>0)", "Selling price must be positive"
    )

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("booking_ids")
    def _compute_booking_count(self):
        for property in self:
            property.booking_count = len(property.booking_ids)

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(record.offer_ids.mapped("price"))
            else:
                record.best_offer = 0

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            if (
                float_compare(
                    record.selling_price,
                    record.expected_price * 0.9,
                    precision_digits=2,
                )
                < 0
            ):
                raise ValidationError(
                    _("Selling price cannot be lower than 90% of the expected price"))

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _unlink_check_state(self):
        for record in self:
            if record.state not in ('new', 'canceled'):
                raise UserError(
                    _("Only New or Cancelled properties can be deleted"))
        return True

    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError(_("Canceled Property cannot be sold"))
            if record.state != "booked":
                raise UserError(
                    _("Property cannot be sold without its booking"))
            record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError(_("Sold Property cannot be canceled"))
            record.state = "canceled"
        return True

    def action_view_booking(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Bookings",
            "res_model": "estate.property.booking",
            "view_mode": "list,form",
            "domain": [
                ("property_id", "=", self.id)

            ],
            "target": "current",
        }

    def booking_sold(self):
        self.ensure_one()
        if self.state == "booked":
            raise UserError(
                _("This property already has an active booking.")
            )

        if self.state in ("sold", "canceled"):
            raise UserError(
                _("A sold or canceled property cannot be booked.")
            )
        booking_wizard_action = {
            'type': 'ir.actions.act_window',
            'res_model': 'estate.property.booking',
            'view_mode': 'form',
            'views': [(False, 'form')],
            'target': 'new',
            'context': {
                "default_property_id": self.id,
                "default_buyer_id": self.buyer_id.id,
                "from_booking_sold": True,
            }
        }
        return booking_wizard_action
