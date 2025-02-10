from odoo import api, fields, models
from datetime import datetime, timedelta
from odoo.exceptions import UserError
class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Model"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default= datetime.now() + timedelta(days=90))
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
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),   
    ])
    active = fields.Boolean(default=False)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ], copy=False, default='new', required=True,)

    # Many2one relationship
    property_type = fields.Many2one('estate.property.type', string="Property Type")
    buyer = fields.Many2one('res.partner', string="Buyer", copy=False)
    seller = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user)

    # Many2many relationship
    tag_ids = fields.Many2many('estate.property.tag', string="Property Tags")

    # One2many relationship
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offer")

    # Computed fields
    total_area = fields.Integer(compute='_compute_total_area', store=True)

    best_price = fields.Float(compute='_compute_best_price', store=True)





    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for data in self:
            data.total_area = data.living_area + data.garden_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for data in self:
            prices = data.offer_ids.mapped('price')
            if prices:
                data.best_price = max(prices)
            else:
                data.best_price = 0.0



    # -------------------------------------------------------------------------
    # ONCHANGE METHODS
    # -------------------------------------------------------------------------

    @api.onchange('garden')
    def _onchange_garden(self):
        """ Set garden area to 10 and orientation to North when garden is True.
            Reset them to empty when garden is False.
        """
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False



    # ------------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------------

    def action_property_sold(self):
        if self.state == 'canceled':
            raise UserError("You cannot sell a canceled property")
        else:
            self.state = 'sold'

        self.active = False
        return True

    def action_property_cancel(self):
        if self.state == 'sold':
            raise UserError("You cannot cancel a sold property")
        else:
            self.state = 'canceled'

        self.active = False
        return True
