from odoo import api, Command, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char(required=True)
    expected_price = fields.Float(required=True)
    description = fields.Text()
    postcode = fields.Char(tracking=1)
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    sold_date = fields.Date(string="Sold Date", readonly=True, copy=False)
    active = fields.Boolean(default=True)
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Orientation",
        selection=[('north', "North"), ('south', "South"), ('east', "East"), ('west', "West")],
        help="The direction the garden faces."
    )
    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('canceled', "Cancelled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default='new',
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
    )
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False,
    )
    salesman_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Tags",
        compute="_compute_tags",
        store=True,
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers",
        copy=True
    )
    issue_ids = fields.One2many(
        'estate.property.issue',
        'property_id',
    )
    visit_ids = fields.One2many(
        "estate.property.visit",
        "property_id",
        string="Visits",
    )
    total_area = fields.Integer(
        compute="_compute_total_area",
        string="Total Area (sqm)",
    )
    best_price = fields.Float(
        compute="_compute_best_price",
        string="Best Offer",
        store=True,
    )
    has_suspicious_offers = fields.Boolean(
        string="Has Suspicious Offers",
        compute="_compute_has_suspicious_offers"
    )
    visit_count = fields.Integer(
        string="Visits Count",
        compute="_compute_visit_count",
        store=True,
    )
    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'Expected price must be strictly positive!',
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'Selling price must be positive!',
    )

    @api.depends("visit_ids")
    def _compute_visit_count(self):
        for record in self:
            record.visit_count = len(record.visit_ids)

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area + record.garden_area
            )

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price")) if record.offer_ids else 0.0

    @api.depends("offer_ids.is_suspicious")
    def _compute_has_suspicious_offers(self):
        for record in self:
            record.has_suspicious_offers = any(
                offer.is_suspicious for offer in record.offer_ids
            )

    @api.depends('expected_price', 'offer_ids', 'sold_date', 'date_availability', 'state')
    def _compute_tags(self):
        for record in self:
            tag_records = self.env['estate.property.tag']

            if record.expected_price > 200000:
                tag_records |= self._get_or_create_tag('High Value')

            if (record.state == 'sold'
                and record.sold_date
                and record.date_availability
                and (record.sold_date - record.date_availability).days <= 10):
                tag_records |= self._get_or_create_tag('Quick Sale')

            if len(record.offer_ids) < 2:
                tag_records |= self._get_or_create_tag('Low Interest')

            record.tag_ids = tag_records

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.constrains('selling_price', 'expected_price')
    def _check_seling_price(self):
        for record in self:
            if float_is_zero(
                record.selling_price,
                precision_digits=2
            ):
                continue
            if float_compare(
                record.selling_price,
                record.expected_price * 0.9,
                precision_digits=2
            ) < 0:
                raise ValidationError("Selling price cannot be lower than 90%"
                                    "of expected price!")

    def action_sold(self):
        for record in self:
            if record.state != 'offer_accepted':
                raise UserError("Accept the property first")
            if record.state == 'canceled':
                raise UserError("Cancelled property cannot be sold!")
            for rec in record.issue_ids:
                if rec.state != 'resolved' and rec.priority == 'high':
                    raise UserError(
                    "Cannot sell the property, please solve the issues"
                )
            record.state = 'sold'
            record.sold_date = fields.Date.today()

        ctx = {
        'default_model': 'estate.property',
        'default_res_ids': self.ids,
        'default_template_id': self.env.ref('estate.email_template_estate_property_sold').id,
        'default_partner_ids': [self.buyer_id.id, self.salesman_id.partner_id.id],
        }

        return {
        'name': 'Sold',
        'type': 'ir.actions.act_window',
        'view_mode': 'form',
        'res_model': 'mail.compose.message',
        'views': [(False, 'form')],
        'view_id': False,
        'target': 'new',
        'context': ctx,
    }

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(
                    "Sold property cannot be cancelled!"
                )
            record.state = 'canceled'
        return True

    def action_create_quotations(self):
        if not self.offer_ids:
            raise UserError("No offers found")

        for offer in self.offer_ids:
            if offer.quotation_id:
                continue
            quotation = self.env["sale.order"].create({
                "partner_id": offer.partner_id.id,
                "origin": self.name,
                "order_line": [
                    Command.create({
                        "name": self.name,
                        "product_uom_qty": 1,
                        "price_unit": offer.price,
                    })
                ],
            })

            offer.quotation_id = quotation.id
        return True

    def _search_tag(self, tag_name):
        return self.env['estate.property.tag'].search(
            [('name', '=', tag_name)], limit=1
        )

    def _create_tag(self, tag_name):
        return self.env['estate.property.tag'].create(
            {'name': tag_name}
        )

    def _get_or_create_tag(self, tag_name):
        return self._search_tag(tag_name) or self._create_tag(tag_name)

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_canceled(self):
        for record in self:
            if record.state not in ('new', 'canceled'):
                raise UserError(
                    "Only new and cancelled properties can be deleted!"
                )
