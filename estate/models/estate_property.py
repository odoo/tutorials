# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Property(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "expecting_price, selling_price, sequence, id"

    name = fields.Char("Name", required=True, translate=True)

    description = fields.Char("Description")

    stage = fields.Selection([
        ("new", "New"),
        ("offer_received", "Offer Received"),
        ("offer_accepted", "Offer Accepted"),
        ("sold", "Sold"),
        ("cancelled", "Cancelled")
    ], default="new", copy=False)

    currency_id = fields.Many2one("res.currency", "Currency")
    expecting_price = fields.Monetary("Expecting Price", required=True)
    best_offer = fields.Monetary("Best Offer", default=0, compute="_compute_best_offer", store=True)
    best_offer_currency_id = fields.Many2one("res.currency", "Best Offer Currency", readonly=True)
    selling_price = fields.Monetary("Selling Price", default=0, readonly=True)

    seller_id = fields.Many2one("res.users", string="Salesperson", index=True, default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", index=True)

    postcode = fields.Integer("Postcode")
    bedroom_number = fields.Integer("Bedrooms", default=0)
    facade_number = fields.Integer("Facades", default=0)
    garage = fields.Boolean("Garage", default=False)
    garden = fields.Boolean("Garden", default=False)

    living_area = fields.Integer("Living Area (sqm)", default=0)
    garden_area = fields.Integer("Garden Area (sqm)", default=0)
    total_area = fields.Integer("Total Area (sqm)", default=0, compute="_compute_total_area", inverse="_inverse_total_area", store=True)

    garden_orientation = fields.Selection([
        ("north", "North"),
        ("south", "South"),
        ("east", "East"),
        ("west", "West")
    ])

    def _current_date(self):
        return fields.Date.today()

    available_from = fields.Date("Date", default=_current_date)

    active = fields.Boolean("Active", default=True)
    sequence = fields.Integer(default=10)

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    property_livable = fields.Boolean("Livable", compute="_compute_property_livable")

    tag_ids = fields.Many2many("estate.tag", string="Tags")

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.onchange("total_area")
    def _inverse_total_area(self):
        for property in self:
            temp_total_area = property.total_area
            property.living_area = max(0, temp_total_area - property.garden_area)
            property.garden_area = temp_total_area - property.living_area

    @api.onchange("garden")
    def _onchange_garden(self):
        for property in self:
            if property.garden:
                property.garden_orientation = "north"
                property.garden_area = 10
            else:
                property.garden_orientation = ""
                property.garden_area = 0

    @api.depends("property_type_id.livable")
    def _compute_property_livable(self):
        for property in self:
            property.property_livable = property.property_type_id.livable

    def _compute_currency(self, offer):
        if offer.currency_id == self.currency_id:
            return offer.price
        return offer.currency_id._convert(offer.price, self.currency_id)

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for property in self:
            temp_best = 0

            best_offer_currency_id = None
            best_offer = 0
            # property.best_offer = max(property.offer_ids.mapped("price"))
            # Could do it if we weren't checking the currencies
            for offer in property.offer_ids:
                val = property._compute_currency(offer)
                if val > temp_best:
                    temp_best = val
                    best_offer_currency_id = offer.currency_id
                    best_offer = offer.price

            property.best_offer = best_offer
            property.best_offer_currency_id = best_offer_currency_id

    _check_bedroom_number = models.Constraint(
        'CHECK(bedroom_number >= 0)',
        'The number of bedrooms can\'t be negative.',
    )

    _check_living_area = models.Constraint(
        'CHECK(living_area >= 0)',
        'The living area can\'t be negative.',
    )

    _check_garden_area = models.Constraint(
        'CHECK(garden_area >= 0)',
        'The garden area can\'t be negative.',
    )

    _check_total_area = models.Constraint(
        'CHECK(total_area >= 0)',
        'The total area can\'t be negative.',
    )
