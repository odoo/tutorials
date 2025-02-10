from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    # Model Configuration
    _name = "estate.property"
    _description = "Estate Property"

    #---------------------------------------------------------------------
    # SQL Constraints
    #---------------------------------------------------------------------
    # _sql_constraints = [
    #     ('check price', 'CHECK(expected_price >= 0)', 'The expected price must be positive')
    # ]

    #---------------------------------------------------------------------
    # Fields
    #---------------------------------------------------------------------
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Integer(string="Postcode")
    date_availability = fields.Date(
        string="Availability Date",
        default=lambda self:fields.Datetime.today() + relativedelta(days=90),
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    best_price = fields.Float(compute="_compute_best_offer", string="Best Offer")
    selling_price = fields.Float(string="Selling Price", default="20000",readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)", default=0)
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area")
    active = fields.Boolean(string="Active",default=True)
    status = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        default="new"
    )

    #---------------------------------------------------------------------
    # Relations
    #---------------------------------------------------------------------

    # Relation for property type
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")

    # Relation for Partner
    user_id = fields.Many2one("res.users", string="Salesmen", copy=False, default = lambda self: self.env.user)
    partner_id = fields.Many2one("res.partner", string="Buyer", readonly=True)

    # Relation for Estate Property Tag
    tag_ids = fields.Many2many("estate.property.tag", string="Tag")

    # Relation for Estate Property Offer
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offer")



    #---------------------------------------------------------------------
    # Compute Methods
    #---------------------------------------------------------------------
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area


    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids.mapped("price"):
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0


    # --------------------------- Onchange Methods ---------------------------    
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""


    # --------------------------- Action Methods ---------------------------
    def action_property_sold(self):
        for record in self:
            if record.status == "cancelled":
                raise UserError("Cancelled property cannot be Sold")
            else:
                record.status = "sold"

    def action_property_cancel(self):
        for record in self:
            if record.status == "sold":
                raise UserError("Sold property cannot be Cancelled")
            else:
                record.status = "cancelled"
                record.partner_id = ""

