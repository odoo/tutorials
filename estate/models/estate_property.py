from datetime import timedelta
from odoo import fields, models, api, exceptions

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy = False,string="Available Form",default = lambda self: fields.Datetime.today() + timedelta(days=90))
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(readonly = True,copy = False, default = 7000000)
    bedrooms = fields.Integer(default = 2)
    living_area = fields.Integer(string = "Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    status = fields.Selection(
        string="Status",
        default = "new",
        copy = False,
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ])
    active = fields.Boolean(default = True)
    property_type_id = fields.Many2one("estate.property.type",string="Property Type")
    property_tag_id = fields.Many2many("estate.property.tag",string="Property Tag")
    buyer_id = fields.Many2one("res.partner",string="Buyer",copy=False)
    salesperson_id = fields.Many2one("res.users",string="Salesman",default=lambda self:self.env.user)
    offer_ids = fields.One2many("estate.property.offer","property_id")
    total_area = fields.Integer(string="Total Area (sqm)", compute = "_compute_total_area", store = True)
    best_offer = fields.Char(compute = "_compute_best_offer", store = True)

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def property_sold(self):
        for record in self:
            if record.status == 'canceled':
                raise exceptions.UserError("A sold property cannot be cancelled!")
            record.status = "sold"
        return True

    def property_cancel(self):
        for record in self:
            if record.status == 'sold':
                raise exceptions.UserError("A sold property cannot be cancelled!")
            record.status = "canceled"
        return True
