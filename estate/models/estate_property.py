from datetime import datetime, timedelta
from odoo import api, fields, models, exceptions, tools


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property's properties"
    _sql_constraints = [
        ('check_expected_price', 'CHECK (expected_price > 0)', 'The expected price must be greater than 0'),
        ('check_selling_price', 'CHECK (selling_price >= 0)', 'The selling price must be greater than 0'),
    ]

    name = fields.Char('Property name', required=True, default='Unknown')
    description = fields.Text('Property Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Availability', copy=False, default=datetime.now() + timedelta(days=90))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection([('North', 'North'), ('East', 'East'), ('South', 'South'), ('West', 'West')], default='North')
    active = fields.Boolean('Active', default=True)
    state = fields.Selection([
        ('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')
    ], default='new', required=True, copy=False)

    total_area = fields.Float("Total Area", compute="_compute_total_area")
    best_price = fields.Float("Best Offer", compute="_compute_best_price")

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    tags_ids = fields.Many2many("estate.property.tag", string="Tags")
    offers_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offers_ids")
    def _compute_best_price(self):
        for record in self:
            best_offer = record._get_best_offer()
            if best_offer is None:
                record.best_price = 0
                return
            record.best_price = best_offer.price

    def _get_best_offer(self):
        if len(self.offers_ids) == 0:
            return None
        best_offer = self.offers_ids[0]
        for offer in self.offers_ids:
            if offer.price > best_offer.price:
                best_offer = offer
        return best_offer

    @api.onchange("garden")
    def _onchange_partner_id(self):
        for record in self:
            if record.garden:
                record.garden_orientation = 'North'
                record.garden_area = 10
            else:
                record.garden_orientation = None
                record.garden_area = 0

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise exceptions.UserError("Can't sell a cancelled offer")
            best_offer = record._get_best_offer()
            if best_offer is None:
                raise exceptions.UserError("The offers for this property are empty")
            self.sold(best_offer)

    def sold(self, offer):
        offer.status = 'accepted'
        self.buyer_id = offer.partner_id
        self.selling_price = offer.price

    def action_cancelled(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError("Can't cancel a sold offer")
            record.state = 'cancelled'

    @api.constrains('selling_price', 'expected_price')
    def _check_date_end(self):
        for record in self:
            if not tools.float_is_zero(record.selling_price, 0e-4) and record.selling_price < record.expected_price * 0.9:
                raise exceptions.ValidationError(
                    f"The selling price cannot be lower than 90% of the expected price (min ${record.expected_price * 0.9}€)")
