from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "id desc"

    name = fields.Char(required=True, index=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda _: fields.Date.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(required=False)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer("Total Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Integer("Best Offer", compute="_compute_best_offer")
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area (sqms)")
    garden_orientation = fields.Selection(
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('west', "West"),
            ('east', "East"),
        ],
        help="Type is used to get the garden orientation in a specific direction",
    )
    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        copy=False,
        default="new",
        tracking=True,
    )
    property_type_id = fields.Many2one("estate.property.type", "Type")
    buyer_id = fields.Many2one("res.partner", copy=False)
    seller_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    tags_ids = fields.Many2many("estate.property.tag", "Tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    active = fields.Boolean(default=True)

    _check_expected_price = models.Constraint(
        "CHECK (expected_price > 0)",
        "A property expected price must be strictly positive",
    )

    _check_selling_price_positive = models.Constraint(
        "CHECK (selling_price >= 0)",
        "A property selling price must be positive",
    )

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        for record in self:
            if record.state not in ("new", "cancelled"):
                raise UserError("Only new and cancelled properties can be deleted.")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        if (
            not float_is_zero(self.selling_price, 2)
            and float_compare(self.selling_price, (self.expected_price * 0.9), 2) == -1
        ):
            raise ValidationError(
                "Selling Price must not be less than 90% of expected price."
            )

    def write(self, vals):
        if "state" in vals:
            new_state = vals["state"]

            for property in self:
                if new_state == "offer_received" and not property.offer_ids:
                    raise ValidationError("A property must have at least one offer.")

                if (
                    new_state == "offer_accepted"
                    and "accepted" not in property.offer_ids.mapped("status")
                ):
                    raise ValidationError(
                        "An offer must be accepted to sell the property."
                    )

                if new_state == "sold":
                    if property.state in ("new", "offer_received"):
                        raise ValidationError(
                            "Accept an offer before selling the property."
                        )

                    if property.state == "cancelled":
                        raise ValidationError(
                            "An estate property cannot be sold if it is already cancelled."
                        )

                if new_state == "cancelled" and property.state == "sold":
                    raise ValidationError(
                        "An estate property cannot be cancelled if it is already sold."
                    )

        return super().write(vals)

    def action_sold_property(self):
        self.ensure_one()
        if self.state == "cancelled":
            raise ValidationError(
                "An estate property cannot be sold which is already marked as cancelled"
            )

        ctx = {
            "default_model": "estate.property",
            # email from
            "default_res_ids": self.ids,
            # email to
            "default_partner_ids": self.buyer_id.ids,
            # "default_composition_mode": "comment",
            # "default_composition_mode": "mass_mail",
        }

        template_id = self.env.ref("estate.email_template_sold")
        if template_id:
            ctx.update({"default_template_id": template_id.id})

        action = {
            "name": self.env._("Send"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "target": "new",
            "context": ctx,
        }

        self.state = "sold"

        return action

    def action_cancel_property(self):
        self.ensure_one()
        if self.state == "sold":
            raise ValidationError(
                "An estate property cannot be cancel which is already marked as sold"
            )

        self.state = "cancelled"
