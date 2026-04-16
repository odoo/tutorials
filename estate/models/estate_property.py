from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Real Estate Property"
    _order = 'id desc'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="living area(sqm)")
    facades = fields.Integer()
    active = fields.Boolean(default=True)
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden area(sqm)")
    garden_orientation = fields.Selection(
        string="Orientation",
        selection=[
            ('north', "North"), ('south', "South"), ('east', "East"), ('west', "West")],
        help="Direction the garden faces"
    )
    tag_ids = fields.Many2many('estate.property.tag', compute='_dynamic_tags', string="Tags")
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    salesperson_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new"
    )
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers", copy=True)
    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_total_area")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")
    issue_ids = fields.One2many('estate.property.issues', 'property_id')

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        for record in self:
            for i in record.issue_ids:
                if i.priority == 'high' and i.issue_state != 'resolved':
                    raise UserError("Cannot sell! Property has unresolved high-priority issues.")
            if record.state == 'cancelled':
                raise UserError("Cancelled properties cannot be sold!")
            record.state = 'sold'
            record.sold_date = fields.Date.today()
        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be cancelled!")
            record.state = 'cancelled'
        return True

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        "The expected price must be strictly positive."
    )
    _check_selling_price_positive = models.Constraint(
        'CHECK(selling_price >= 0)',
        "The selling price must be positive."
    )

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            if float_compare(
                record.selling_price,
                record.expected_price * 0.90,
                precision_digits=2
            ) < 0:
                raise ValidationError(
                    "The selling price cannot be lower than 90% of the expected price."
                )

    sold_date = fields.Date()
    sold_within = fields.Integer(string='Sold Within (Days)', compute='_compute_sold_within', store=True)

    @api.depends('sold_date', 'create_date')
    def _compute_sold_within(self):
        for record in self:
            if record.sold_date and record.create_date:
                record.sold_within = (record.sold_date - record.create_date.date()).days
            else:
                record.sold_within = 0

    @api.depends('expected_price', 'offer_ids', 'sold_within')
    def _dynamic_tags(self):
        all_tags = self.env['estate.property.tag'].search([('name', 'in', ('High Value', 'Quick Sale', 'Low Interest'))])

        if 'High Value' not in all_tags.mapped('name'):
            all_tags |= self.env['estate.property.tag'].create({'name': 'High Value'})

        if 'Low Interest' not in all_tags.mapped('name'):
            all_tags |= self.env['estate.property.tag'].create({'name': 'Low Interest'})

        if 'Quick Sale' not in all_tags.mapped('name'):
            all_tags |= self.env['estate.property.tag'].create({'name': 'Quick Sale'})

        high_value_tag = all_tags.filtered(lambda t: t.name == 'High Value')
        low_interest_tag = all_tags.filtered(lambda t: t.name == 'Low Interest')
        quick_sale_tag = all_tags.filtered(lambda t: t.name == 'Quick Sale')

        for record in self:
            tags_to_add = self.env['estate.property.tag']
            if record.expected_price > 1000:
                tags_to_add |= high_value_tag
            if len(record.offer_ids) < 2:
                tags_to_add |= low_interest_tag
            if record.sold_within and record.sold_within <= 10:
                tags_to_add |= quick_sale_tag
            record.tag_ids = [(6, 0, tags_to_add.ids)]

    @api.ondelete(at_uninstall=False)
    def _check_state_before_delete(self):
        for property in self:
            if property.state not in ('new', 'cancelled'):
                raise UserError(
                    "You cannot delete a property that is not 'New' or 'Cancelled'."
                )

    has_suspicious_offers = fields.Boolean(string="Has Suspicious Offers", compute="_compute_has_suspicious_offers", store=False)

    @api.depends('offer_ids.suspicious_offer')
    def _compute_has_suspicious_offers(self):
        for record in self:
            record.has_suspicious_offers = any(offer.suspicious_offer for offer in record.offer_ids)

    visit_ids = fields.One2many('estate.property.visit', 'property_id', string="Visits")
    visit_count = fields.Integer(string="Visit Count", compute='_compute_visit_count')

    @api.depends('visit_ids')
    def _compute_visit_count(self):
        for record in self:
            record.visit_count = len(record.visit_ids)
