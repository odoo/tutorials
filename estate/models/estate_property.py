from odoo import fields, models, api
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate model"
    name = fields.Char(required=True)
    salesman_id = fields.Many2one("res.partner", string="Salesman")
    buyer_id = fields.Many2one("res.users", default=lambda self: self.env.user, string="Buyer")
    type_id = fields.Many2one("estate.property.type")
    tags_id = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    active = fields.Boolean(default=True)
    state = fields.Selection(
        required=True,
        copy=False,
        default="new",
        selection=[("new", "New"), ("offer received", "Offer Received"), ("offer accepted", "Offer Accepted"), ("sold", "Sold"), ("cancelled","Cancelled")]
    )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Datetime(copy=False, default=fields.Datetime.today() + (relativedelta(months=3)))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='type',
        selection=[('north', 'North'), ('south', 'South'), ('East', 'east'), ('West', 'west')]
    )
    total_area = fields.Integer(string="Total Area", compute="_compute_total_surface")
    best_offer = fields.Float(string="Best Offer", compute="_compute_best_offer")


    #==========computed fields===============
    @api.depends('garden_area', 'living_area')
    def _compute_total_surface(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped("price"))

    #============onchage fields==============
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = False
            self.garden_orientation = False


