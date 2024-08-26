from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'The Real Estate Advertisement module'

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqrm)')
    facades = fields.Integer('Fcades')
    garage = fields.Boolean(string="Garage", default=False)
    garden = fields.Boolean(string="Garden", default=False)
    garden_area = fields.Integer('Garden Area', default=0)
    expected_price = fields.Float('Expected Price', required=True)
    active = fields.Boolean(default=True)
    sales_man_id = fields.Many2one("res.users", string="Salesmam", default=lambda self: self._uid)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    type_id = fields.Many2one("estate.property.type", string="Type")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offer")
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area (sqrm)")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")
    date_availability = fields.Date(
        'Availability Date',
        copy=False,
        default=fields.Datetime.add(fields.Datetime.today(), months=3),
    )

    selling_price = fields.Float(
        'Selling Price',
        readonly=True,
        copy=False,
    )

    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        string='Garden Orientation',
    )
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_Received", "Offer Received"),
            ("offer_Accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        default="New",
        required=True,
        copy=False,
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold_property(self):
        pass
