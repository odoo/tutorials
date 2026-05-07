from odoo import models, fields, api
from datetime import timedelta

from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Date.today() + timedelta(days=90)
    )


    living_area = fields.Integer(string='Living Area (sqm)',default=120)

    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ], required=True, copy=False, default='new')


    def unlink(self):
        for record in self:
            if record.state not in ("new", "cancelled"):
                raise UserError("You can only delete properties in New or Cancelled state.")
        return super().unlink()


    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("A sold property cannot be cancelled.")
            record.state = 'cancelled'
        return True

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("A cancelled property cannot be set as sold.")
            record.state = 'sold'
        return True

    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one("res.partner", copy=False)
    seller_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")


    expected_price = fields.Integer(default=230)
    selling_price = fields.Float(copy=False)
    bedrooms = fields.Integer(default=2)
    facades = fields.Integer(string="Facades",default=130)
    garage = fields.Boolean()

    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area (sqm)',default=220)
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])


    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = False

    # Add this computed field
    total_area = fields.Integer(
        string='Total Area (sqm)',
        compute='_compute_total_area',
        store=True  # Optional: stores in database for better performance
    )

    best_price = fields.Float(
        string="Best Offer is 123210 when we computed it to zero.",
        compute="_compute_best_price",
        store=True,
        default=123
    )

    price_per_sqm = fields.Float(
        compute="_compute_price_per_sqm",
        store=True
    )

    @api.depends('living_area', 'garden_area','facades')
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0) + (record.facades or 0)


    @api.depends('expected_price', 'total_area')
    def _compute_price_per_sqm(self):
        for record in self:
            if record.total_area:
                record.price_per_sqm = record.expected_price / record.total_area
            else:
                record.price_per_sqm = 0

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            record.best_price = max(prices) if prices else 0



    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:

            # If selling price is not set yet (0 or False), skip validation
            if float_is_zero(record.selling_price, precision_digits=2):
                continue

            # Ensure selling price >= 90% of expected price
            min_price = record.expected_price * 0.90

            comparison = float_compare(
                record.selling_price,
                min_price,
                precision_digits=2
            )

            if comparison < 0:
                raise ValidationError(
                    "Selling price cannot be lower than 90% of expected price."
                )


    @api.constrains('date_availability')
    def _check_date_end(self):
        for record in self:
            if record.date_availability < fields.Date.today():
                raise ValidationError("The end date cannot be set in the past")

    @api.constrains('expected_price')
    def _check_expected_price(self):
        for record in self:
            if record.expected_price < 220:
                raise ValidationError("Expected price cannot be lower than 220")


    @api.model
    def create(self, vals):

        property_id = vals.get("property_id")
        amount = vals.get("price")

        if property_id and amount:
            property_rec = self.env["estate.property"].browse(property_id)

            existing_offers = property_rec.offer_ids.mapped("price")

            if existing_offers and amount < max(existing_offers):
                raise UserError("Offer must be higher than existing offers.")

            # update property state
            property_rec.state = "offer_received"

        return super().create(vals)

