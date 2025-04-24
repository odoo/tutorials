from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property discription"

    name = fields.Char('name', required=True)
    description = fields.Text('description', compute="_compute_description")
    postcode = fields.Char('postcode')
    availability_date = fields.Date(
        'availabilty date', copy=False, default=fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float('expected price', required=True)
    selling_price = fields.Float('selling price', readonly=True, copy=False)
    bedrooms = fields.Integer('bedrooms', default=2)
    living_area = fields.Integer('living area')
    facades = fields.Integer('facades')
    garage = fields.Boolean('garage')
    garden = fields.Boolean('garden')
    garden_area = fields.Integer('garden area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'),
                   ('east', 'East'), ('west', 'West')]
    )
    active = fields.Boolean('active', default=True)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'),
                   ('offer_accepted', 'Offer Acccepted'), ('sold', 'Sold'),
                   ('cancelled', 'Cancelled')],
        default="new"
    )
    property_type_id = fields.Many2one(
        "estate.property.type", string="property type")
    user_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many(
        "estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute='_compute_total_area')
    best_offer = fields.Float(compute="_compute_best_offer")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("buyer_id")
    def _compute_description(self):
        for record in self:
            record.description = "Description for buyer %s" % record.buyer_id.name

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        try:
            for record in self:
                if len(record.offer_ids) > 0:
                    record.best_offer = max(record.offer_ids.mapped("price"))
                else:
                    record.best_offer = 0.0
        except Exception as e:
            print(e)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None
