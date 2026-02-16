# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Property(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "expecting_price, selling_price, sequence, id"

    name = fields.Char("Name", required=True, translate=True)

    property_type = fields.Selection(
        [
            ("house", "House"),
            ("apartment", "Apartment"),
            ("land", "Land")
        ],
        required=True
    )

    currency_id = fields.Many2one('res.currency', 'Currency', readonly=True)
    expecting_price = fields.Monetary("Expecting Price", required=True)
    selling_price = fields.Monetary("Selling Price", default=0)

    bedroom_number = fields.Integer("Bedrooms", default=0)
    area = fields.Integer("Living Area (sqm)", required=True)

    sequence = fields.Integer(default=10)

    tag_ids = fields.Many2many("estate.tag", string="Tags")

    _check_bedroom_number = models.Constraint(
        'CHECK(bedroom_number >= 0)',
        'The number of bedrooms can\'t be negative.',
    )

    _check_area = models.Constraint(
        'CHECK(area >= 0)',
        'The area can\'t be negative.',
    )
