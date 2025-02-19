from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, tools 
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _name = "estate.property"
    _inherit = ["mail.thread"]
    _description = "Real Estate Property"

    name = fields.Char(string="Property Name", required=True,tracking=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False, default=None,tracking=True)
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user,tracking=True
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    tag_ids = fields.Many2many("estate.property.tags", string="Property Tags")
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers",
    )
    date_availability = fields.Date(
        string="Availability Date",
        default=lambda self: fields.Date.today() + relativedelta(months=3),
    )
    expected_price = fields.Float(string="Expected Price", required=True, default=0.0)
    selling_price = fields.Float(string="Selling Price")
    image = fields.Image(string="Image",max_width=1920,max_height=1920)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Float(string="Living Area (sq.m.)")
    facades = fields.Integer(string="Number of Facades")
    garage = fields.Boolean(string="Has Garage")
    garden = fields.Boolean(string="Has Garden")
    garden_area = fields.Float(string="Garden Area (sq.m.)")
    total_area = fields.Float("Total Area", compute="_compute_total_area")
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="State",
        tracking=True,
        group_expand=True
    )
    best_price = fields.Float(
        "Best Buyer Price", compute="_compute_best_price", store=True
    )
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
        string="Garden Orientation",
    )

    # SQL Constraints
    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "Expected price must be positive",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "The selling price must be positive.",
        ),
    ]

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if record.selling_price:
                if (
                    tools.float_compare(
                        record.selling_price,
                        record.expected_price * 0.9,
                        precision_digits=2,
                    )
                    < 0
                ):
                    raise UserError(
                        "Selling price must be at least 90% of the expected price!"
                    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _check_when_detele_record(self):
        for record in self:
            if record.state not in ["new", "cancelled"]:
                raise UserError(
                    "You cannot delete a property that is not 'New' or 'Cancelled'."
                )

    def action_cancel_property(self):
        if self.state == "sold":
            raise UserError("Sold properties cannot be cancelled.")
        self.state = "cancelled"

    def action_set_sold(self):
        if self.state == "cancelled"  :
            raise UserError("Cancelled properties cannot be sold.")
        if self.state != "offer_accepted":   
            raise UserError("property can not be sold without accepting offer.")
        self.state = "sold"
        if self.buyer_id.email:
            template=self.env.ref('estate.estate_property_sold_email_template')
            template.send_mail(self.id,)