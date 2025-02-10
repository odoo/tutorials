from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError,ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"
    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Date Availability",
        copy=False,
        default=lambda self: fields.Date.today() + timedelta(days=90),
    )
    expected_price = fields.Float(string="Expected Price")
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Number of Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (m²)")
    facades = fields.Integer(string="Number of Facades")
    garage = fields.Boolean(string="Has Garage")
    garden = fields.Boolean(string="Has Garden", default=True)
    garden_area = fields.Integer(string="Garden Area (m²)")
    garden_orientation = fields.Selection(
        [  # this list contains all drop-down options
            ("north", "North"),  # (internal_value,Displayed value)
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Orientation",
        copy=False,
    )
    active = fields.Boolean(string="Active", default=True)
    status = fields.Selection(
        [  # this list contains all drop-down options
            ("new", "New"),  # (internal_value,Displayed value)
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        string="Status",
        default="new",
        copy=False,
    )

    
    def unlink(self):
        for record in self:
            if record.status not in ['new', 'canceled']:
                raise UserError(f"Cannot delete the property '{record.name}' because its state is '{record.state}'.")
        
        # After applying the business logic, call the parent unlink() method
        return super(EstateProperty, self).unlink()

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    # property_seller_id=fields.Many2one('estate.property.seller',string="Salesman")
    # property_buyer_id=fields.Many2one('estate.property.buyer',string="Buyer")
    property_seller_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    property_buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(string="Total Area", compute="_compute_total_area")
    best_price = fields.Float(string="Best Price", compute="_compute_best_price")

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0:
                    raise ValidationError("The selling price cannot be lower than 90% of the expected price.")

    '''@api.constrains('expected_price')
    def _check_expected_price(self):
        for record in self:
            if record.expected_price<=0:
                raise ValidationError("Expected price should strictly be positive")

    @api.constrains('selling_price')
    def _check_expected_price(self):
        for record in self:
            if record.selling_price<=0:
                raise ValidationError("Expected price should strictly be positive")'''

    _sql_constraints = [
    ('check_expected_price', 'CHECK(expected_price > 0)', 'Expected price should strictly be positive'),
    ('check_selling_price', 'CHECK(selling_price >= 0)', 'Selling price should strictly be positive')
        ]


    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 1000
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def sold_event(self):
        for record in self:
            if record.status != 'sold':  # Prevent selling if already sold
                record.status = 'sold'
            else:
                raise UserError("This property is already sold.")
        return True

    def cancel_event(self):
        for record in self:
            if record.status != 'canceled':  # Only allow cancel if not canceled
                record.status = 'canceled'
            else:
                raise UserError("This property is already canceled.")
        return True
