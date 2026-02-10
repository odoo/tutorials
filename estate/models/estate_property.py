import datetime
from odoo import api, fields, models, exceptions
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = "estate.estate.property"
    _description = "Real Estate Property Module Tutorial"
    _order = "id desc"

    ## SQL Constraints Section ##

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price should be a positive number'
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price should be a positive number'
    )

    name = fields.Char(
        "Property Name",
        required=True,
        help="Enter the name of the property"
    )
    active = fields.Boolean(default=True)
    description = fields.Text(
        "Property Description",
        help="Enter a quick description of the characteristic of the property"
    )
    postcode = fields.Char(
        "Postcode",
        help="Enter the postcode of the property"
    )
    date_availability = fields.Date(
        "Date Availability",
        copy=False,
        help="Enter the date at which the property is available. By default set to 3 months",
        default=lambda _: fields.Date.today() + datetime.timedelta(weeks=12)    # Equivalent to 3 months
    )
    expected_price = fields.Float(
        "Expected Price",
        required=True,
        help="The expected price for the property."
    )
    selling_price = fields.Float(
        "Selling Price",
        readonly=True,
        copy=False,
        default=0.0,
    )
    bedrooms = fields.Integer(
        "Nb Bedrooms",
        default=2,
        help="The number of bedrooms that the property has. By default set to 2."
    )
    living_area = fields.Integer(
        "Living Area",
        help="The number of square meters the living area has."
    )
    facades = fields.Integer(
        "Nb Facades",
        help="The number of facades the property has. Cannot be more that four."
    )
    garage = fields.Boolean(
        "Garage",
        help="Is the property has a garage?"
    )
    garden = fields.Boolean(
        "Garden",
        help="Is the property has a garden?"
    )
    garden_area = fields.Integer(
        "Nb Garden Area",
        help="Enter the number of square meters the garden has. Only if the property has a garden"
    )
    garden_orientation = fields.Selection(
        string="Orientation",
        selection = [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="Choose the orientation of the garden"
    )
    state = fields.Selection(
        string="State",
        selection = [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required = True,
        copy = False,
        default="new",
    )
    # Property Type ID
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        help="The type of the property (House, Loft, Apartment, etc.)"
    )
    # Buyer and Salesperson
    salesperson = fields.Many2one(
        "res.users",
        string="Salesperson",
        index=True,
        default=lambda self: self.env.user,
        help="Name of the salesperson"
    )    # Internal entity
    buyer = fields.Many2one(
        "res.partner",
        string="Buyer",
        index=True,
        copy=False,
        help="Name of the potential buyer for the property"
    )    # External entity

    # Tags as Many2many
    tags_ids = fields.Many2many(
        "estate.property.tag",
        string="Tags"
    )

    # Offers as One2many
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers",
    )
    total_area = fields.Float(
        compute="_compute_total_area",
        string="Total Area (sqm)",
        help="Total area of the property"
    )
    best_offer = fields.Float(
        compute="_compute_best_offer",
        string="Best Offer",
        help="The best offer proposed so far"
    )

    ## API Constraints Section ##

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, 2) and float_compare(record.selling_price, record.expected_price * 0.9, 4) < 0 :
                raise exceptions.ValidationError("The selling price cannot be less than 90% of the expected price!")

    ## Method Section ##

    def sold_property_action(self):

        if not self.env.user.has_group('estate.group_system'):
            exceptions.UserError("You do not have permission to perform this action!")

        for record in self:
            if record.state != "cancelled":
                record.state = "sold"
            else:
                raise exceptions.UserError("A cancelled property cannot be sold!")
        return True

    def cancel_property_action(self):
        for record in self:
            if record.state != "sold":
                record.state = "cancelled"
            else:
                raise exceptions.UserError("A sold property cannot be cancelled!")
        return True

    ## CRUD Methods ##
    @api.ondelete(at_uninstall=True)
    def property_delete_checker(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise exceptions.UserError("Cannot delete the property except if it's 'new' or 'cancelled' one!")
        return True


    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(record.offer_ids.mapped('price'))
            else:
                record.best_offer = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    @api.onchange("offer_ids")
    def _onchange_offers(self):
        if self.offer_ids and self.state == "new":
            self.state = "offer_received"
        if len(self.offer_ids) == 0:
            self.state = "new"

    @api.onchange("state")
    def _onchange_state(self):
        if self.state == "cancelled" or self.state == "sold":
            self.active = False
        else:
            self.active = True
