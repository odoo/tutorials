from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero


class Property(models.Model):
    _name = 'estate.property'
    _description = 'Estate property'
    _order = 'id desc'

    name = fields.Char("Name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From", copy=False, default=lambda x: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Type",
        selection=[('north', "North"), ('south', "South"), ('east', "East"), ('west', "West")],
    )
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        string="Status",
        selection=[('new', "New"), ('offer_received', "Offer Received"), ('offer_accepted', "Offer Accepted"), ('sold', "Sold"), ('cancelled', "Cancelled")],
        default='new',
        required=True,
        copy=False,
    )
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    user_id = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    property_tag_ids = fields.Many2many('estate.property.tag')
    property_offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Float(compute='_compute_total_area')
    best_offer = fields.Float(compute="_compute_best_offer")

    _sql_constraints = [
        ('positive_expected_price', 'CHECK(expected_price > 0)', "A property expected price must be strictly positive"),
        ('positive_selling_price', 'CHECK(selling_price >= 0)', "A property selling price must be positive"),
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('property_offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            if not record.property_offer_ids:
                record.best_offer = 0
            else:
                record.best_offer = max(record.property_offer_ids.mapped('price'))

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_set_sold(self):
        for record in self:
            if self.state == 'cancelled':
                raise UserError(_("Property is cancelled and cannot be sold."))

            record.state = 'sold'

        return True

    def action_set_cancelled(self):
        for record in self:
            if self.state == 'sold':
                raise UserError(_("Sold properties cannot be cancelled."))

            record.state = 'cancelled'
            record.active = False

        return True

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            min_selling_price = record.expected_price * 0.9

            if not float_is_zero(record.selling_price, precision_digits=2) and float_compare(record.selling_price, min_selling_price, precision_digits=2) < 0:
                raise UserError(_(
                    "The selling price must be at least 90 percent of the expected price! You must reduce the expected price if you want to accept this offer."
                    ))
