from odoo import api, fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property"

    name = fields.Char(required= True)
    description = fields.Text()
    property_type_id = fields.Many2one(comodel_name="estate.property.type", copy=False)
    postcode = fields.Char("Postal Code", copy=False)
    date_availability = fields.Date(default=lambda self: fields.Date.add(fields.Date.today(), months=3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ("new", "New"),
        ("offer_recieved", "Offer recieved"),
        ("offer_accepted", "Offer accepted"),
        ("sold", "Sold"),
        ("canceled", "Canceled"),    
    ], default="new", required=True, copy=False)
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')], help="Select orientation between the four cardinal points")
    total_area = fields.Integer(compute="_compute_total_area", )
    buyer_id = fields.Many2one(comodel_name="res.partner", ondelete="restrict")
    salesperson_id = fields.Many2one(string="sales person id", comodel_name="res.users", ondelete="restrict", default=lambda self: self.env.user)
    property_tag_ids = fields.Many2many(string="tags", comodel_name="estate.property.tag")
    offer_ids = fields.One2many(comodel_name="estate.property.offer", inverse_name="property_id")
    best_offer = fields.Float(compute="_compute_best_offer", default=0)


    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for property in self:
            property.best_offer = max(property.offer_ids.mapped("price"), default=0) 
          

    @api.onchange("garden")
    def _onchange_partner_id(self):
        for property in self:
            property.garden_area = self.garden and 10
            property.garden_orientation = self.garden and "north"
       
