from odoo import api,fields,models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "See properties"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default= lambda self:fields.Date.add(fields.Date.today(), months=3),copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Type',
        selection=[('north','North'),
                ('east','East'),
                ('west','West'),
                ('south','South')]
    )
    active = fields.Boolean(default="True")
    state = fields.Selection(
        selection=[('new','New'), 
                   ('offer_recieved','Offer Recieved'), 
                   ('offer_accepted','Offer Accepted'), 
                   ('sold','Sold'),
                   ('cancelled','Cancelled')],
        required=True,
        copy=False,
        default='new'
    )

    property_type_id = fields.Many2one("estate.property.type", string="Property Types")
    buyer_id = fields.Many2one("res.partner", string="seller")
    seller_id = fields.Many2one("res.users", string="buyer", default=lambda self: self.env.user)
    property_tag_ids = fields.Many2many("estate.property.tags", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer","property_id", string="Offers")

    total_area = fields.Float(compute="_compute_total_area",store=True)
    best_price = fields.Float(compute="_compute_best_price",store=True)

    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False
