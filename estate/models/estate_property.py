from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: fields.Date.add(fields.Date.today(), months=3),
                                    copy=False,
                                    string="Available From")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    active = fields.Boolean(default=True)
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_direction = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orientation"
        )
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        default='new',
        required=True,
        copy=False
    )
    type_id = fields.Many2one("estate.property.type", string="Property Type")
    tag_ids = fields.Many2many("estate.property.tag", string="Tag")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offer")
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area (sqm)")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)
            
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_direction = 'north'
        else:
            self.garden_area = False
            self.garden_direction = False
    
    def action_estate_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(self.env._("A cancelled property cannot be set as sold"))
            record.state = 'sold'
        return True

    def action_estate_cancelled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(self.env._("A sold property cannot be set as cancelled"))
            record.state = 'cancelled'
        return True
