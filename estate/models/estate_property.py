from odoo import models, fields, api, exceptions
from datetime import timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate properties"
    _order = "id desc"

    name = fields.Char("Name", readonly=False, required=True)
    description = fields.Text("Description", readonly=False)
    
    postcode = fields.Char("Postcode", readonly=False)
    date_availability = fields.Date("Available From", readonly=False, copy=False, default=lambda self: fields.Date.today() + timedelta(days=90))
    
    expected_price = fields.Float("Expected Price", readonly=False, required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    
    bedrooms = fields.Integer("Bedrooms", readonly=False, default=2)
    living_area = fields.Integer("Living Area", readonly=False)
    
    facades = fields.Integer("Facades", readonly=False)
    
    garage = fields.Boolean("Garage", readonly=False)
    garden = fields.Boolean("Garden", readonly=False)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    garden_area = fields.Integer("Garden Area", readonly=False)
    
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help = "The garden orientation is used to describe Garden's orientation, lol?"
    )

    total_area = fields.Integer("Total Area", readonly=True, compute="_compute_total_area", store=True)

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    active = fields.Boolean("Active", default=True)

    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        default="new",
        string="Status",
        required=True,
        readonly=True
    )

    seller_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)

    property_type_id = fields.Many2one("estate.property.type", string="Type", ondelete='cascade')
    property_tags_id = fields.Many2many("estate.property.tag", string="Tags", ondelete='cascade')

    offer_ids = fields.One2many("estate.property.offer", inverse_name="property_id")

    best_price = fields.Float("Best Offer", readonly=True, compute="_compute_best_price", store=True)

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    def action_mark_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise exceptions.UserError('A Cancelled Property Cannot Be Sold')
            else:
                record.state = 'sold'

    def action_mark_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError('A Sold Property Cannot Be Cancelled')
            else:
                record.state = 'cancelled'

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price should be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price > 0)', 'The selling price should be strictly positive.')
    ]

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < 0.9 * record.expected_price:
                exceptions.ValidationError(r'The selling price is lower than the 90% of expected price.')

    @api.constrains('offer_ids')
    def _check_offers(self):
        for record in self:
            if record.offer_ids:
                if record.state == 'new':
                    record.state = 'offer_received'
