from odoo import fields, models, api
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'The estate property'
    _order = 'id desc'

    name = fields.Char("Property name", required=True)
    description = fields.Text()
    postcode = fields.Char()
    active = fields.Boolean(default=True)
    date_availability = fields.Date(default=fields.Date.add(fields.Date.today(), months=3))

    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Float(compute='_compute_total_area', store=True)
    best_offer = fields.Float(compute='_compute_best_price')

    garden_orientation = fields.Selection(
        string="Garden orientation",
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('west', "West"),
            ('east', "East"),
        ],
    )
    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('canceled', "Canceled"),
        ],
        required=True,
        copy=False,
        default='new',
    )
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    seller_id = fields.Many2one('res.users', string="Seller", default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

    _sql_constraints = [
        (
            'expected_price_positive',
            'CHECK(expected_price > 0)',
            "The expected price must be strictly positive.",
        ),
        (
            'selling_price_positive',
            'CHECK(selling_price >= 0)',
            "The selling price must be positive.",
        ),
    ]

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            max_price = 0
            for offer in record.offer_ids:
                if offer.price > max_price:
                    max_price = offer.price
            record.best_offer = max_price

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be cancelled.")
            record.state = 'canceled'
        return True

    @api.ondelete(at_uninstall=False)
    def unlink(self):
        if self.filtered(lambda x: x.state not in ['new', 'canceled']):
            raise UserError("Only property in New/Canceled state can be deleted from database.")

    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("Cancelled properties cannot be sold.")
            record.state = 'sold'
        return True
