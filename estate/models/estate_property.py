from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available from", copy=False, default=lambda self: fields.Date.today() + timedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")

    garden_orientation = fields.Selection(
        [
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West")
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled")
        ],
        string="Status", required=True, copy=False, default='new')

    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    seller_id = fields.Many2one('res.users', string="Seller", default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tags', string="Property tags", compute="_compute_tags", store=True)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', copy=True)
    total_area = fields.Integer(string="Total Area", compute="_compute_total_area", store=True)
    best_price = fields.Integer(string="Best Offer", compute="_compute_best_price", store=True)

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'Expected price must be positive.'
    )

    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'Selling price must be positive.'
    )

    @api.depends('offer_ids', 'expected_price', 'offer_ids.status', 'create_date', 'state')
    def _compute_tags(self):
        tags = self.env['estate.property.tags'].search([])
        a = tags.filtered(lambda t: t.name == 'Low Interest')
        b = tags.filtered(lambda t: t.name == 'High Value')
        c = tags.filtered(lambda t: t.name == 'Quick Sale')

        # a = self.env['estate.property.tags'].search([('name', '=', 'Low Interest')],limit=1)
        # b = self.env['estate.property.tags'].search([('name', '=', 'High Value')],limit=1)
        # c = self.env['estate.property.tags'].search([('name', '=', 'Quick Sale')],limit=1)

        if len(a) == 0:
            a = self.env['estate.property.tags'].create({'name': 'Low Interest'})
        if len(b) == 0:
            b = self.env['estate.property.tags'].create({'name': 'High Value'})
        if len(c) == 0:
            c = self.env['estate.property.tags'].create({'name': 'Quick Sale'})

        for record in self:
            tag_ids = []
            if len(record.offer_ids) <= 2:
                tag_ids.append(a.id)
            if record.expected_price > 100:
                tag_ids.append(b.id)
            if record.create_date and record.state == 'sold':
                diff = (fields.Date.today() - record.create_date.date()).days
                if diff <= 10:
                    tag_ids.append(c.id)

            record.tag_ids = tag_ids

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area, self.garden_orientation = 10, 'north'
        else:
            self.garden_area, self.garden_orientation = 0, False

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Cancelled property cannot be sold.")
            record.state = 'sold'
        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold property cannot be cancelled.")
            record.state = 'cancelled'

    @api.constrains("selling_price", "expected_price")
    def check_price(self):
        for record in self:
            if record.selling_price > 0 and (record.selling_price < record.expected_price * 0.9):
                raise ValidationError("You cannot set a selling price below 90 percent of the expected price")
