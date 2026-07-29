from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"

    def _default_date_availability(self):
        return fields.Date.today() + relativedelta(months=3)

    active = fields.Boolean(default=True)
    bedrooms = fields.Integer(default=2)
    best_price = fields.Float(
        compute="_compute_best_price",
        search="_search_best_price",
    )
    buyer = fields.Many2one("res.partner", copy=False)
    date_availability = fields.Date(
        copy=False,
        default=_default_date_availability,
    )
    description = fields.Text(translate=True)
    expected_price = fields.Float(required=True, tracking=True)
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(
        compute="_compute_garden_details",
        store=True,
        readonly=False,
    )
    garden_orientation = fields.Selection(
        [('north', "North"), ('south', "South"), ('east', "East"), ('west', "West")],
        compute="_compute_garden_details",
        store=True,
        readonly=False,
    )
    living_area = fields.Integer()
    maintenance_ids = fields.One2many(
        "estate.property.maintenance",
        "property_id",
        string="Maintenance",
    )
    name = fields.Char(required=True, translate=True)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="offers")
    postcode = fields.Char()
    property_type = fields.Many2one("estate.property.type")
    sales_person = fields.Many2one("res.users", default=lambda self: self.env.user)
    selling_price = fields.Float(readonly=True, copy=False)
    sq_area = fields.Float(compute="_compute_computed_area")

    state = fields.Selection(
        [
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    tag_ids = fields.Many2many(
        "estate.property.tag",
        compute="_compute_dynamic_tags",
        store=True,
        readonly=False,
    )
    total_area = fields.Integer(compute="_compute_total_area")

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "The expected price of property should be positive.",
    )
    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)",
        "Offer price of property should be positive.",
    )

    @api.depends('expected_price', 'state', 'offer_ids')
    def _compute_dynamic_tags(self):
        now = fields.Datetime.now()

        tag_names = ['high value', 'quick sell', 'low interest']
        existing_tags = self.env['estate.property.tag'].search(
            [('name', 'in', tag_names)],
        )

        tags_dict = {tag.name: tag for tag in existing_tags}
        for name in tag_names:
            if name not in tags_dict:
                tags_dict[name] = self.env['estate.property.tag'].create({'name': name})

        for record in self:
            create_date = record.create_date or now

            new_tags = self.env['estate.property.tag']

            if record._origin:
                new_tags |= tags_dict['low interest']

            if record.expected_price > 2_00_000:
                new_tags |= tags_dict['high value']

            if (create_date + relativedelta(days=10)) <= now and record.state == 'sold':
                new_tags |= tags_dict['quick sell']

            if len(record.offer_ids) <= 2:
                new_tags |= tags_dict['low interest']

            record.tag_ids |= new_tags

    @api.onchange("state")
    def _onchange_state_validation(self):
        if self.state == 'sold' and self._origin.state == 'cancelled':
            self.state = 'cancelled'
            raise ValidationError(message="cancelled properties cannot be sold")

    def _search_best_price(self, operator, value):
        groups = self.env["estate.property.offer"]._read_group(
            domain=[],
            groupby=["property_id"],
            aggregates=["price:max"],
            having=[("price:max", operator, value)],
        )
        property_ids = [res_group[0].id for res_group in groups if res_group[0]]
        return [("id", "in", property_ids)]

    @api.depends("total_area")
    def _compute_computed_area(self):
        for property in self:
            property.sq_area = property.total_area**2

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for property in self:
            prices = property.offer_ids.mapped("price")
            property.best_price = max(prices) if prices else 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area, self.garden_orientation = 10, "north"
        else:
            self.garden_area, self.garden_orientation = 0, False

    @api.depends("garden")
    def _compute_garden_details(self):
        for property in self:
            if property.garden:
                property.garden_area, property.garden_orientation = 10, "north"
            else:
                property.garden_area, property.garden_orientation = 0, False

    def action_set_state_cancel(self):
        for record in self:
            record.state = "cancelled"
        return True

    def action_set_state_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError(self.env._("cancelled properties cannot be sold"))
            record.state = "sold"
        return True

    def action_set_best_price(self):
        for property in self:
            offer_id = property.offer_ids.filtered(
                lambda o: o.price == property.best_price,
            )
            offer_id.action_accept()

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for prop in self:
            if float_is_zero(prop.selling_price, precision_digits=2):
                continue

            min_allowed_price = prop.expected_price * 0.90

            if (
                float_compare(prop.selling_price, min_allowed_price, precision_digits=2)
                == -1
            ):
                raise ValidationError(
                    message="The selling price cannot be lower than 90% of the expected price!",
                )

    @api.ondelete(at_uninstall=False)
    def _unlink_property(self):
        if any(property.state in ['new', 'cancelled'] for property in self):
            raise UserError(
                message="you can't delete a property with state 'new' and 'cancelled'!",
            )
