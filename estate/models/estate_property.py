from odoo import api, models, fields
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property test model'

    def _get_availability_default():
        today = fields.Date.today()
        return fields.Date.add(today, months=3)

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=_get_availability_default())
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('west', 'West'),
        ('south', 'South'),
        ('east', 'East')
    ])
    active = fields.Boolean(default=False)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('received', 'Offer Received'),
            ('accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ], 
        required=True, 
        readonly=True, 
        default='new'
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    user_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    type_id = fields.Many2one("estate.property.type", string="Property Type")
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area (sqm)")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if(self.garden):
            self.garden_orientation = self.garden_orientation or 'north'
            self.garden_area = self.garden_area or 10
        else:
            self.garden_orientation = None
            self.garden_area = None

    @api.onchange("garden_orientation", "garden_area")
    def _onchange_garden_info(self):
        if(self.garden_orientation or self.garden_area):
            self.garden = True
        else:
            self.garden = False

    def cancel_property(self):
        for property in self:
            if property.state == 'sold':
                raise UserError(self.env._("You cannot set a previously sold property as Cancelled"))
            property.state = "cancelled"
        return True

    def sell_property(self):
        for property in self:
            if property.state == 'cancelled':
                raise UserError(self.env._("You cannot set a previously cancelled property as Sold"))
            property.state = "sold"
        return True
