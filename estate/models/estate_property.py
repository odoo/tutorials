from datetime import timedelta

from odoo import models, fields, api

from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    _order = "id desc"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available From", copy=False, default=lambda self: fields.Date.today() + timedelta(days=90))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)", copy=False)
    total_area = fields.Integer(string="Total Area (sqm)", compute="_compute_total_area", store=True)
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_orientation = fields.Selection(
        [
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ],
        string="Garden Orientation"
    )
    garden_area = fields.Integer(string="Garden Area (sqm)")
    active = fields.Boolean(string="is Active", default=True)
    state = fields.Selection(
        [
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled")
        ],
        string="Status", required=True, copy=False, default='new', readonly=False)
    swimming_pool = fields.Boolean(string="Swimming Pool")
    property_age = fields.Integer(string="Property Age")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tags_ids = fields.Many2many("estate.property.tag", string="Property Tags", compute="_compute_tags", readonly=False)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    issue_ids = fields.One2many("estate.property.issue", "property_id", string="Issue")
    visit_ids = fields.One2many("estate.property.visit", "propert_id", string="visit")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")
    spam = fields.Boolean(string="is suspicious", compute="_compute_offers")
    overdue = fields.Boolean(string="Issue Overdue")

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'Expected price must be strictly positive.'
    )

    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'Selling price must be positive.'
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            record.best_price = max(prices) if prices else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = False

    @api.depends("expected_price", "offer_ids", "state", "create_date")
    def _compute_tags(self):
        Tag = self.env['estate.property.tag']
        tag_names = ['high value', 'low interest', 'quick sale']
        tags = Tag.search([('name', 'in', tag_names)])
        tag_map = {}
        for tag in tags:
            tag_map[tag.name] = tag
        for name in tag_names:
            if name not in tag_map:
                tag_map[name] = Tag.create({'name': name})
        high = tag_map['high value']
        low = tag_map['low interest']
        quick = tag_map['quick sale']

        today = fields.Date.today()
        for record in self:
            new_tags = self.env['estate.property.tag']
            if record.expected_price > 200:
                new_tags |= high
            if len(record.offer_ids) <= 2:
                new_tags |= low
            if record.state == 'sold':
                calc = (today - record.create_date.date()).days
                if calc <= 10:
                    new_tags |= quick
            record.tags_ids = new_tags

    @api.depends("offer_ids.partner_id", "offer_ids.create_date")
    def _compute_offers(self):
        for record in self:
            record.spam = False
            for offers in record.offer_ids:
                count = 0
                for other_offer in record.offer_ids:
                    if other_offer.partner_id == offers.partner_id and other_offer.create_date and offers.create_date:
                        if abs(other_offer.create_date - offers.create_date) <= timedelta(minutes=5):
                            count += 1
                if count >= 3:
                    record.spam = True
                    break

    @api.constrains("selling_price", "expected_price")
    def _set_price(self):
        for record in self:
            if record.selling_price > 0 and record.selling_price < 0.9 * record.expected_price:
                raise ValidationError("Selling price cannot be lower than 90 percent of expected price.")

    @api.constrains("visit_ids")
    def _single_partner(self):
        for record in self:
            for other_date in record.visit_ids:
                for current_date in record.visit_ids:
                    if current_date.id != other_date.id:
                        if other_date.visit_date < current_date.end_date and current_date.visit_date < other_date.end_date:
                            raise ValidationError("only 1 partner in 1 day")

    @api.ondelete(at_uninstall=False)
    def _property_deletion(self):
        for record in self:
            if record.state not in ('new', 'cancelled'):
                raise UserError("You can only delete properties in New or Cancelled state.")

    def action_sold(self):
        for record in self:
            for issue in record.issue_ids:
                if issue.priority == 'high' and issue.state == 'overdue':
                    raise UserError("property cannot sold due to overdue")
            if record.state == 'cancelled':
                raise UserError("Cancelled property cannot be sold.")
            if record.state != 'offer_accepted':
                raise UserError("Property cannot be sold without an accepted offer.")

            record.state = 'sold'
        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold property cannot be cancelled.")
            record.state = 'cancelled'
        return True
