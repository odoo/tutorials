from datetime import timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Description"
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'A property expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'A property selling price must be positive.')
    ]
    _order = 'id desc'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: fields.Date.today() + timedelta(days=90), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string="Garden Orientation",
        help="Select One Orientation"
    )
    active = fields.Boolean(default=False)
    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        required=True,
        copy=False,
        default='new'
    )

    # property Many2one realtion with type
    property_type_id = fields.Many2one(
        'estate.property.type',
        string='Property Types'
    )

    seller_id = fields.Many2one(
        'res.users',
        string="Salesman",
        default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one(
        'res.partner',
        copy=False,
        string="Buyer"
    )

    # property Many2many realtion with tag
    tag_ids = fields.Many2many(
        'estate.property.tag',
        string="Proprty Tag"
    )

    # property One2many realtion with offer
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
    )

    # store the total area by living_area and garden_area
    total_area = fields.Integer(compute="_compute_totalArea")

    # store the best price of offers
    # if we use store=True then it saves the computed value in database too
    best_offer_price = fields.Integer(compute="_compute_bestPrice", store=True)

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price != 0.0 and record.selling_price < 0.9 * self.expected_price:
                raise ValidationError("selling price cannot be lower than 90% of the expected price.")

    # function for compute the total area
    @api.depends("living_area", "garden_area")
    def _compute_totalArea(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    # function for compute the best price of offers
    @api.depends("offer_ids.price")
    def _compute_bestPrice(self):
        for record in self:
            record.best_offer_price = max(record.offer_ids.mapped("price"), default=0)

    # change in value of garden(Boolean) reflects garden_area and garden_orientation automatically
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_property_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("This property is already Cancelled.")
            else:
                record.state = 'sold'
        return True

    def action_property_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("This property is already Sold.")
            else:
                record.state = 'canceled'
        return True

    @api.ondelete(at_uninstall=False)
    def _prevent_delete_new_canceled(self):
        if self.state not in ['new', 'canceled']:
            raise UserError("You can not delete a property which is not new or canceled.")
