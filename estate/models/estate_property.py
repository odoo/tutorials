from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Properties Table"
    _order = "id desc"
    _inherit = ['mail.thread.cc',
                'mail.activity.mixin',
               ]

    name = fields.Char(string="Property Name", required=True)
    image = fields.Binary(string="Image")
    email = fields.Char(index='trigram')
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: fields.Date.today() + relativedelta(months=3),
    )
    expected_price = fields.Monetary(required=True, tracking=True)
    selling_price = fields.Monetary(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
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
        required=True,
        copy=False,
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    seller_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        copy=False,
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(string="Total Area", compute="_compute_total_area")
    best_price = fields.Monetary(compute="_compute_best_price", store=True)
    currency_id = fields.Many2one(
        "res.currency", default=lambda self: self.env.company.currency_id,
    )

    _check_expected_price_positive = models.Constraint(
        "CHECK(expected_price > 0 AND selling_price >= 0)",
        "The property expected price and selling price must be higher than 0",
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        for record in self:
            if record.state not in ("new", "cancelled"):
                raise UserError(
                    _("properties can not be deleted if they are not new or cancelled"),
                )

    def action_sold(self):
        self.ensure_one()
        if self.state == "cancelled":
            raise UserError(_("Cancelled properties can not be sold."))
        self.state = "sold"

        message = "Property is sold"
        return {
            "effect": {
                "fadeout": "slow",
                "message": message,
                "img_url": "/web/static/img/smile.svg",
                "type": "rainbow_man",
            },
        }

        return True

    def action_cancel(self):
        self.ensure_one()
        if self.state == "sold":
            raise UserError(_("Sold properties can not be cancelled."))
        self.state = "cancelled"
        return True
