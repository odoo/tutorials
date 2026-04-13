from odoo import fields, models, api


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char(string="Name", required=True, default="Unknown")
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    description = fields.Text(string="Description")
    date_availability = fields.Date(string="Available From", copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    postcode = fields.Char(string="Postcode", required=True)
    expected_price = fields.Float(string="Expected Price")
    selling_price = fields.Float(string="Selling Price", readonly=True)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden_area")
    garden_orientation = fields.Selection(string="Garden Orientation", selection=[("north", "North"), ("east", "East"), ("west", "West"), ("south", "South")])

    # If it is false then newly created record won't be appear. but record is created when active is set true record will appear.
    active = fields.Boolean("Active", default=True)
    # State can get selected and as copy is set False in duplicate it cannot get copied
    state = fields.Selection(string="state", selection=[("new", "New"), ("offer_received", "Offer Received"), ("accepted", "Accepted"), ("sold", "Sold"), ("cancelled", "Cancelled")], default="new", copy=False)
    property_type_id = fields.Many2one("estate.property.type", string="Property type")
    buyer_id = fields.Many2one(comodel_name="res.partner", string="Buyer", copy=False, default=lambda self: self.env.user.partner_id)
    sales_person = fields.Many2one(comodel_name="res.users", string="Sales person", index=True, tracking=True, default=lambda self: self.env.user)
    property_tag = fields.Many2many(comodel_name="estate.property.tag", string="Property Tags")
    offer_id = fields.One2many(comodel_name="estate.property.offer", inverse_name="property_id", string="Property offer")

    total_area = fields.Integer(string="total_area", name="Total area", compute="_compute_total")

    @api.depends("garden_area", "living_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area
