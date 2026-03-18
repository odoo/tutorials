from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "date_availability desc"
    _inherit = ["mail.thread"]

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=lambda self: fields.Date.today() + timedelta(days=90),
        copy=False,
    )
    event_id = fields.Many2one('event.event', string="Open House Event")
    expected_price = fields.Float(required=True, default=0.0)
    selling_price = fields.Float(readonly=True, copy=False)
    best_price = fields.Float(compute="_compute_best_price")
    bedrooms = fields.Integer(default=2, copy=False)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Float(compute="_compute_total_area", store=True)
    squared_area = fields.Float(compute="_compute_squared_area", store=True)
    garden_orientation = fields.Selection(
        [
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', "New"),
        ('offer_received', "Offer Received"),
        ('offer_accepted', "Offer Accepted"),
        ('sold', "Sold"),
        ('cancelled', "Cancelled"),
    ],
    tracking=True, default='new')
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
    )
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False,
        readonly=True,
    )
    user_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers",
    )
    request_ids = fields.One2many(
        "estate.request",
        "request_id",
        string="Requests",
    )
    request_count = fields.Integer(
        string="Request Count",
        compute="_compute_request_count",
        store=True,
    )

    _expected_price_check = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price must be strictly positive.'
    )
    _selling_price_check = models.Constraint(
        'CHECK(selling_price IS NULL OR selling_price >= 0)',
        'The selling price must be positive.'
    )
    visit_ids = fields.One2many(
        "estate.property.visit",
        "property_id",
        string="Visits"
    )
    visit_count = fields.Integer(compute="_compute_visit_count")

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)

        for record in records:
            event = self.env['event.event'].create({
                'name': f"Open House - {record.name}",
                'date_begin': fields.Datetime.now(),
                'date_end': fields.Datetime.now() + timedelta(hours=2),
                'property_id': record.id,
            })

            record.event_id = event.id  

        return records
    
    def _compute_visit_count(self):
        Visit = self.env['estate.property.visit']
        for record in self:
            record.visit_count = Visit.search_count([
                ('property_id', 'in', record.ids)
            ])

    @api.depends("total_area")
    def _compute_squared_area(self):
        for record in self:
            record.squared_area = record.total_area**2

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            record.best_price = max(prices) if prices else 0.0

    @api.depends('request_ids')
    def _compute_request_count(self):
        for rec in self:
            rec.request_count = len(rec.request_ids)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _ondelete_check_state(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError(
                    f"Cannot delete property '{record.name}' with state '{record.state}'. "
                    f"Only properties in 'New' or 'Cancelled' state can be deleted."
                )

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for property in self:
            if float_is_zero(property.selling_price, precision_digits=2):
                continue
            minimum_price = property.expected_price * 0.9
            if float_compare(
                property.selling_price,
                minimum_price,
                precision_digits=2
            ) < 0:
                raise ValidationError(
                    "The selling price cannot be lower than 90% of the expected price."
                )

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold property cannot be cancelled.")
            record.state = "cancelled"

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Cancelled property cannot be sold.")
            accepted_offer = record.offer_ids.filtered(
                lambda offer: offer.status == 'accepted'
            )
            if not accepted_offer:
                raise UserError("You must accept an offer before selling the property.")
            record.state = 'sold'

            contract = self.env['estate.contract'].search([
                ('property_id', '=', record.id)
            ], limit=1)

            if not contract:
                raise UserError("No contract found.")

            if not contract.sign_request_id or contract.sign_request_id.state != 'signed':
                raise UserError("Contract is not signed yet.")


            record.state = 'sold'

    def best_accept(self):
        for record in self:
            best = 0
            for offer in record.offer_ids:
                if offer.price > best:
                    best_record = offer
                    best = offer.price
            best_record.action_accept()
    
    def action_open_event(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Open House Events',
            'res_model': 'event.event',
            'view_mode': 'list,form',  
            'domain': [('property_id', '=', self.id)],  
            'context': {
                'default_property_id': self.id  
            },
        }
