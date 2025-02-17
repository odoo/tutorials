from dateutil.relativedelta import relativedelta
from odoo import api, exceptions, fields, models, tools


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate model"
    _inherit = ['mail.thread']
    _order = "id desc"
    
    _sql_constraints = [
        ('positive_expected_price', 'CHECK(expected_price > 0)','The expected price must be positive.'),
        ('positive_selling_price', 'CHECK(selling_price > 0)','The selling price must be positive.')
    ]

    name = fields.Char(string="Name", required=True, tracking=True)
    description = fields.Text(string="Description", required=True)
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Date Availability", copy=False, default=lambda self: fields.Datetime.today()+relativedelta(days=90))
    expected_price = fields.Float(string="Expected Price")
    selling_price = fields.Float(string="Selling Price", copy=False, readonly=True)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden", default=False)
    garden_area = fields.Integer(string="Garden Area")
    last_seen = fields.Datetime(string="Last Seen", default=fields.Datetime.now())
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"), 
            ("south", "South"), 
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type", string="Property Type")
    buyer_id = fields.Many2one(
        comodel_name="res.partner", string="Buyer", copy=False, readonly=True)
    salesperson_id = fields.Many2one(
        comodel_name="res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many(
        comodel_name="estate.property.tag", string="Tags")
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer", inverse_name="property_id")
    total_area = fields.Float(compute="_compute_total_area" ,store=True)
    best_price = fields.Integer(compute="_compute_best_price")
    company_id = fields.Many2one(
        comodel_name='res.company', string="Company", default=lambda self: self.env.user.company_id,
        required=True)

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
        
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0.0)

    @api.constrains("selling_price") #expected price removed as it not required.
    def _check_selling_price(self):
        for record in self:
            # if(len(record.offer_ids) == 0): alternate approach
            #     pass
            if not record.offer_ids:
                pass
            elif(record.selling_price<(0.9*record.expected_price)):
                raise exceptions.ValidationError("Selling prices should atleast be 90 percent of the expected price.")
            else:
                pass

    @api.onchange("garden")
    def _onchange_garden_area(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None
    
    @api.ondelete(at_uninstall=False)
    def _unlink_if_property_is_new_or_cancelled(self):
        for record in self:
            if record.state in ['offer received', 'offer accepted', 'sold']:
                raise exceptions.UserError("Only new and cancelled properties can be deleted.")

    def action_cancel_property(self):
        for record in self:
            if record.state != "sold":
                record.state = "cancelled"
            else:
                raise exceptions.UserError("Property is already sold!")
        return True

    def action_sell_property(self):
        for record in self:
            if record.state != "cancelled" and record.state == "offer_accepted":
                record.state = "sold"
                record.message_post(body=("Congratulations! It's sold."))
            else:
                raise exceptions.UserError("Sorry! This list cannot be sold at this stage.")
        return True
