# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Property(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "expecting_price, selling_price, sequence, id"

    name = fields.Char("Name", required=True, translate=True)

    """property_type = fields.Selection(
        [
            ("house", "House"),
            ("apartment", "Apartment"),
            ("land", "Land")
        ],
        required=True
    )"""

    description = fields.Char("Description")

    stage = fields.Selection([
        ("new", "New"),
        ("offer_received", "Offer Received"),
        ("offer_accepted", "Offer Accepted"),
        ("sold", "Sold"),
        ("cancelled", "Cancelled")
    ], default="new", copy=False)

    currency_id = fields.Many2one('res.currency', 'Currency', readonly=True)
    expecting_price = fields.Monetary("Expecting Price", required=True)
    best_offer = fields.Monetary("Best Offer", default=0)
    selling_price = fields.Monetary("Selling Price", default=0, readonly=True)

    seller_id = fields.Many2one("res.users", string="Salesperson", index=True, default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", index=True)

    postcode = fields.Integer("Postcode")
    bedroom_number = fields.Integer("Bedrooms", default=0)
    facade_number = fields.Integer("Facades", default=0)
    garage = fields.Boolean("Garage", default=False)
    garden = fields.Boolean("Garden", default=False)

    living_area = fields.Integer("Living Area (sqm)", default=0)
    total_area = fields.Integer("Total Area (sqm)", default=0)

    def _current_date(self):
        return fields.Date.today()

    available_from = fields.Date("Date", default=lambda self: self._current_date())

    active = fields.Boolean("Active", default=True)
    sequence = fields.Integer(default=10)

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    property_livable = fields.Boolean("Livable", compute="_compute_property_livable")

    tag_ids = fields.Many2many("estate.tag", string="Tags")

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    @api.depends("property_type_id.livable")
    def _compute_property_livable(self):
        for property in self:
            property.property_livable = property.property_type_id.livable

    _check_bedroom_number = models.Constraint(
        'CHECK(bedroom_number >= 0)',
        'The number of bedrooms can\'t be negative.',
    )

    _check_living_area = models.Constraint(
        'CHECK(living_area >= 0)',
        'The living_area can\'t be negative.',
    )

    _check_total_area = models.Constraint(
        'CHECK(total_area >= 0)',
        'The total_area can\'t be negative.',
    )
