from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = " Real estate Property"

    def _default_validity(self):
        return fields.Date.today() + relativedelta(months=+3)

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    name = fields.Char(required=True, default="UNKNOWN")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=_default_validity, copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean(default=True)
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string="Garden Orientation"
    )
    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        default='new',
        copy=False,
        required=True,
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="property type",
    )
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
    )
    user_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    tags_ids = fields.Many2many(
        "estate.property.tag",
        string="tags",
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
    )
    total_area = fields.Float(compute="_compute_total_area")
