from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _inherit=["mail.thread","mail.activity.mixin"]
    _order = "id desc"
    name = fields.Char(string="Property Name", required=True,tracking=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode",tracking=True)
    date_availability = fields.Date(
        string="Date Availability",
        copy=False,
        default=lambda self: fields.Date.today() + timedelta(days=90),
    )
    expected_price = fields.Float(string="Expected Price",tracking=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False,tracking=True)
    bedrooms = fields.Integer(string="Number of Bedrooms", default=2,tracking=True)
    living_area = fields.Integer(string="Living Area (m²)",tracking=True)
    facades = fields.Integer(string="Number of Facades",tracking=True)
    garage = fields.Boolean(string="Has Garage")
    garden = fields.Boolean(string="Has Garden")
    garden_area = fields.Integer(string="Garden Area (m²)",tracking=True)
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
    active = fields.Boolean(string="Active", default=True,tracking=True)
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
        tracking=True,
    )


    property_type_id = fields.Many2one("estate.property.type", string="Property Type",tracking=True)
    # property_seller_id=fields.Many2one('estate.property.seller',string="Salesman")
    # property_buyer_id=fields.Many2one('estate.property.buyer',string="Buyer")
    property_seller_id = fields.Many2one(
        "res.users", string="Salesman",tracking=True,default=lambda self: self.env.user
    )
    property_buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False,tracking=True)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags",tracking=True)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers",tracking=True)
    total_area = fields.Float(string="Total Area", compute="_compute_total_area",tracking=True)
    best_price = fields.Float(string="Best Price", compute="_compute_best_price",tracking=True)
    company_id = fields.Many2one(
        'res.company',
        required=True,
        string="Company",
        default=lambda self: self.env.company,
        tracking=True
    )

    def unlink(self):
        for record in self:
            if record.status not in ["new", "canceled"]:
                raise UserError(
                    f"Cannot delete the property '{record.name}' because its state is '{record.state}'."
                )

        # After applying the business logic, call the parent unlink() method
        return super(EstateProperty, self).unlink()

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                if (
                    float_compare(
                        record.selling_price,
                        record.expected_price * 0.9,
                        precision_digits=2,
                    )
                    < 0
                ):
                    raise ValidationError(
                        "The selling price cannot be lower than 90% of the expected price."
                    )

    """@api.constrains('expected_price')
    def _check_expected_price(self):
        for record in self:
            if record.expected_price<=0:
                raise ValidationError("Expected price should strictly be positive")

    @api.constrains('selling_price')
    def _check_expected_price(self):
        for record in self:
            if record.selling_price<=0:
                raise ValidationError("Expected price should strictly be positive")"""

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "Expected price should strictly be positive",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "Selling price should strictly be positive",
        ),
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
        if self.status != "canceled" and self.status == "offer_accepted":  # Prevent selling if already sold
            self.status = "sold"
        else:
            raise UserError("This property is already sold.")

    def cancel_event(self):
        if self.status != "canceled":  # Only allow cancel if not canceled
            self.status = "canceled"
        else:
            raise UserError("This property is already canceled.")
        return True

    # this will called when the status is changed (as we wrote tracking=True inside status) and will return to the xml files's id where we mention view/message what we have to show on the chatter. 
    def _track_subtype(self,init_values):
        if 'status' in init_values and self.status == 'sold':
            return self.env.ref('estate.propery_sold_chatter')
        return super()._track_subtype(init_values)
    
