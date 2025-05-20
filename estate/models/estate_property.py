from odoo import api, fields, models
from dateutil.relativedelta import relativedelta

class Estate_property(models.Model):
    _name = "estate.property"
    _description = "Model to modelize Real Estate objects"

    name = fields.Char(string="Name", required=True)
    description  = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Datetime(copy=False, default=fields.date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north','North'), ('south','South'),('east','East'),('west','West')],
        help="Orientation is meant to describe the garden"
    )
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string='Status',
        selection=[('new','New'), ('offer_received','Offer Received'),('offer_accepted','Offer Accepted'),('sold','Sold'),('cancelled', 'Cancelled')],
        help="Orientation is meant to describe the garden",
        default='new',
        copy=False
    )
    buyer_id = fields.Many2one("res.partner")
    seller_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    property_type_id = fields.Many2one("estate.property.type")
    property_tag_ids = fields.Many2many("estate.property.tags")
    property_offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_area")
    best_offer_price = fields.Float(compute="_compute_best_offer")

    @api.depends("garden_area", "living_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("property_offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer_price = max(p.price for p in record.property_offer_ids)

    @api.onchange("garden")
    def _onchange_partner_id(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = "north" if self.garden else None