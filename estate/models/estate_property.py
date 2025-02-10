from odoo import models, fields, api
from odoo.exceptions import UserError

class EstateProperty(models.Model):

    # ..................private attribute..................
    _name = "estate.property"
    _description = "These are Estate Module Properties"

    # ..................fields attribute..................
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Date Availability", default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price")
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ('n', 'North'),
            ('s', 'South'),
            ('e', 'East'),
            ('w', 'West')
        ],
        string="Garden Orientation"
    )
    state = fields.Selection(
        string="Status", 
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        default='new',
        copy=False, 
        required=True
    )
    active = fields.Boolean(string="Active", default=True)

    property_type_id = fields.Many2one(comodel_name="estate.property.type", string="Property Type")
    property_tag_ids = fields.Many2many(comodel_name="estate.property.tag", string="Tags")
    property_offer_ids = fields.One2many(comodel_name="estate.property.offer", inverse_name="property_id", string="Offers", default=[])
    user_id = fields.Many2one(comodel_name='res.users', string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one(comodel_name='res.partner', string='Buyer', copy=False)

    total_area = fields.Integer(string="Total Area (sqm)", compute="_compute_total_area")
    best_price = fields.Float(string="Best Price", compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("property_offer_ids.price")
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.property_offer_ids.mapped("price")) if property.property_offer_ids else 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "n"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        if self.state == "cancelled":
            raise UserError("Cancelled properties cannot be sold")
        else:
            self.state = "sold"
        return True

    def action_cancel(self):
        if self.state == "sold":
            raise UserError("Sold properties cannot be cancelled")
        else:
            self.state = "cancelled"
        return True
