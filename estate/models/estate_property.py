from odoo import api, fields, models, _


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char('Title', required=True)
    active = fields.Boolean('Active', default=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available From', copy=False,
                                    default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Number of Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Number of Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(string='Garden orientation', selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    state = fields.Selection(string='Status',
                             selection=[('new', 'New'), ('received', 'Offer Received'), ('accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
                             default='new',
                             copy=False,
                             required=True
    )
    total_area = fields.Integer("Total Area", compute="_compute_total_area")
    best_offer = fields.Float("Best Offer", compute="_compute_best_offer")

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer = fields.Many2one("res.partner", string="Buyer")
    salesperson = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    # ------------------------------------------------------------
    # COMPUTED FIELDS
    # ------------------------------------------------------------

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price')) if record.offer_ids else 0.0

    # ------------------------------------------------------------
    # CONSTRAINTS AND ONCHANGES
    # ------------------------------------------------------------

    @api.onchange("garden")
    def _onchange_garden(self):
        self.ensure_one()
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = False
        else:
            self.garden_area = 10
            self.garden_orientation = 'north'
