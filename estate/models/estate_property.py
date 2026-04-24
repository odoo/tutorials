from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer received"),
            ("offer_accepted", "Offer accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        copy=False,
    )
    name = fields.Char(
        required=True,
        string="Title",
    )
    description = fields.Text(
        string="Description",
    )
    postcode = fields.Char(
        string="Postcode",
    )
    date_availability = fields.Date(
        default=fields.Date.add(fields.Date.today(), months=3),
        copy=False,
        string="Available from",
    )

    expected_price = fields.Float(
        string="Expected price",
    )
    selling_price = fields.Float(
        string="Selling price",
        readonly=True,
        copy=False,
        default_export_compatible=False,
    )

    bedrooms = fields.Integer(default=2, string="Bedrooms")
    living_area = fields.Integer(string="Living Area", default=0)
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    has_garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area", default=0)
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="If you don't know where West is, wait for the sun to go to sleep. Its bedroom lies West.",
    )

    customer_id = fields.Many2one("res.partner", string="Customer", copy=False)

    salesman_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user,
        required=True,
    )
    estate_property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
    )

    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="estate_property_id",
    )

    best_price = fields.Float(
        string="Best Offer",
        compute="_compute_best_price",
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for ep in self:
            ep.total_area = (
                ep.living_area + ep.garden_area if ep.has_garden else ep.living_area
            )

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for ep in self:
            ep.best_price = max(ep.offer_ids.mapped("price")) if ep.offer_ids else None

    @api.onchange("has_garden")
    def _onchange_has_garden(self):
        if self.has_garden:
            self.garden_area = 10
            self.garden_orientation = "north"

    def action_set_accepted(self):
        # todo: split action and validation (validation goes into python constraint)
        for ep in self:
            # ideally this should refined but this is a tutorial so I think it s ok as is
            accepted_offers = ep.offer_ids.filtered(lambda o: o.status == "accepted")
            if (
                ep.state in ("offer_accepted", "sold", "cancelled")
                or len(accepted_offers) != 1
            ):
                raise UserError(
                    _("Wrong status or there s something wrong with accepted offers"),
                )

            ep.state = "offer_accepted"

    def action_set_sold(self):
        # todo: split action and validation (validation goes into python constraint)
        for ep in self:
            if ep.state == "cancelled":
                raise UserError(_("A cancelled property cannot be sold"))
            accepted_offers = ep.offer_ids.filtered(lambda o: o.status == "accepted")

            if ep.state != "offer_accepted" or len(accepted_offers) < 1:
                raise UserError(
                    _(
                        "Make sure to have an accepted offer before setting the property as sold",
                    ),
                )
            if len(accepted_offers) > 1:
                raise UserError(
                    _(
                        "Multiple accepted offers - fix this before marking the property as sold",
                    ),
                )

            assert len(accepted_offers) == 1

            ep.state = "sold"
            ep.customer_id = accepted_offers[0].partner_id
            ep.selling_price = accepted_offers[0].price

        return True

    def action_set_cancelled(self):
        # todo: split action and validation (validation goes into python constraint)
        for ep in self:
            # todo later : add warning - dont know how to do this from the model
            if ep.state == "sold":
                raise UserError(_("A cancelled property cannot be sold"))
            ep.state = "cancelled"
        return True
