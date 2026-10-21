from odoo import api, exceptions, fields, models
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate properties declaration"

    active = fields.Boolean(default=True)
    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=(fields.Date.today() + relativedelta(months=3)), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[
            ('north', 'North'),
            ('east', 'East'),
            ('south', 'South'),
            ('west', 'West')
            ],
        help="Orientation is used to specify how the garden is oriented with the house."
    )
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')
        ],
        help="State is used to specify the progress of the current estate offer",
        required=True,
        default='new',
    )
    type_id = fields.Many2one("estate.property.type", string="Property type")
    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Propety tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offer(s)")

    # -------------------------------------------------------------
    # Constraints
    # -------------------------------------------------------------
    _check_expected_price_strict_positive = models.Constraint(
    'CHECK(expected_price > 0)',
    'The expected price of a property should be greater than 0.',
    )

    _check_selling_price_positive = models.Constraint(
    'CHECK(selling_price >= 0)',
    'The selling price of a property should be positive.',
    )

    # -------------------------------------------------------------
    # Computed field and their method
    # -------------------------------------------------------------
    total_area = fields.Integer(compute="_compute_total_area")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_offer = fields.Float(compute="_compute_best_offer")

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price')) if record.offer_ids else 0.0

    # -------------------------------------------------------------
    # Onchange actions
    # -------------------------------------------------------------
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None
            
    # ------------------------------------------------------------- 
    # UI actions
    # -------------------------------------------------------------
    def action_flag_property_as_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise exceptions.UserError('Canceled properties cannot be sold')
            else:
                record.state = 'sold'
        return True

    def action_flag_property_as_canceled(self):
        for record in self:
            record.state = 'canceled'
        return True
        