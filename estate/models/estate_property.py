from odoo import api, exceptions, fields, models, tools


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(string="Property Name", required=True)
    description = fields.Char(string="Property Description")
    postcode = fields.Char(string="Postal Code")
    date_availability = fields.Date(
        string="Available From",
        default=fields.Date.add(value=fields.Date.today(), months=3),
        copy=False,
    )
    expected_price = fields.Float(string="Expected Selling Price", required=True)
    selling_price = fields.Float(
        string="Actual Selling Price", readonly=True, copy=False,
    )
    bedrooms = fields.Integer(string="Number of Bedrooms", default=2)
    living_area = fields.Float(string="Living Area (sqm)")
    facades = fields.Integer(string="Number of Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Float(string="Garden Area (sqm)", compute="_automate_garden")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        compute="_automate_garden",
    )
    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_area")
    active = fields.Boolean(string="Active", default=True)
    status = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        copy=False,
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    user_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    partner_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    property_tag_ids = fields.Many2many("estate.property.tag", string="Property Tag")
    property_offers_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    best_offer = fields.Float(string="Best Offer", compute="_compute_best_offer")

    @api.depends("living_area", "garden_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("property_offers_ids.price")
    def _compute_best_offer(self):
        for record in self:
            # for offer in record.property_offers_ids:
            #     best_offer= max(offer.price, best_offer)
            record.best_offer = max(record.mapped("property_offers_ids.price"), default=0)

    @api.onchange("garden")
    def _automate_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None

    def sell_apartment(self):
        for record in self:
            if record.status == "cancelled":
                raise exceptions.UserError("Cancelled apartments can not be sold")
            record.status = "sold"
        return True

    def cancel_apartment(self):
        for record in self:
            if record.status == "sold":
                raise exceptions.UserError("Sold apartments can not be cancelled")
            record.status = "cancelled"
        return False
    
    # @api.constrains("expected_price")
    # def _check_expected_price(self):
    #     for record in self:
    #         if record.expected_price < 0:
    #             raise exceptions.ValidationError("Enter a valid expected price")
    
    _check_expected_price = models.Constraint(
        'CHECK(expected_price >= 0)',
        'The expected price of an should be greater than 0.',
    )

    @api.constrains("expected_price","selling_price")
    def _check_valid_transaction(self):
        for record in self:
            if record.property_offers_ids:
                print(record.property_offers_ids)
                if tools.float_compare(record.selling_price, 0.9*record.expected_price, 2) < 1:
                    raise exceptions.ValidationError("Selling price can not be less than 90% of your expected price. Lower your expected price to accept this transaction.")
