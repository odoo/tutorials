from odoo import fields, models, api
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Real Estate Property"

    active = fields.Boolean(string="Active", default=True)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    best_price = fields.Float(string="Best Offer", compute='_compute_best_price')
    date_availability = fields.Date(
        string="Available From",
        default=lambda self: fields.Date.add(fields.Date.context_today(self), months=3),
        copy=False
    )
    description = fields.Text(string="Description")
    expected_price = fields.Float(string="Expected Price", required=True)
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West")
        ],
        string="Garden Orientation",
        help="Direction the garden faces"
    )
    living_area = fields.Integer(string="Living Area (sqm)")
    name = fields.Char(string="Title", required=True)
    postcode = fields.Char(string="Postcode")
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    state = fields.Selection(
        [
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        string="State",
        required=True,
        default='new',
        copy=False
    )
    total_area = fields.Integer(string="Total Area",
                                compute='_compute_total_area',
                                store=True)

    # Many2one: property type (House, Apartment, etc.)
    property_type_id = fields.Many2one(
        'estate.property.type',
        string='Property Type'
    )

    # Many2one: buyer (from res.partner — contacts)
    buyer_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        copy=False
    )

    # Many2one: salesperson (from res.users — Odoo users)
    salesperson_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        default=lambda self: self.env.user
    )

    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string='Offers'
    )

    tag_ids = fields.Many2many(
        'estate.property.tag',
        string='Tags'
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for rec in self:
            rec.best_price = max(rec.offer_ids.mapped('price'), default=0.0)

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
            if record.state == 'cancelled':
                raise UserError("Cancelled properties cannot be sold.")
            record.state = 'sold'
        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be cancelled.")
            record.state = 'cancelled'
        return True
