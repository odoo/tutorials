from odoo import api,fields,models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class estate_property(models.Model):
    # Private attributes
    _name = "estate.property"
    _description = "Estate property file"
    _order = "id desc"

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The expected price should be strictly positive.'),
        ('check_property_selling_price','CHECK(selling_price>=0)',
         'Property selling price should be posiive')
    ]

    # Default methods
    def _default_date_availability(self,number_of_months):
        return fields.Date.context_today(self) + relativedelta(months=number_of_months)

    # Fields declaration
    name = fields.Char('Name',required=True, translate=True, default='Unknown')
    description = fields.Text("Description",required=True, translate=True)
    postcode = fields.Char("Post code",required=False, translate=True)
    date_avaibility = fields.Date("Avaibility date",required=False, copy=False, default=lambda self: self._default_date_availability(3))
    expected_price = fields.Float("Expected Price",required=False)
    selling_price = fields.Float("Selling Price",readonly=True, copy=False, required=False)
    bedrooms = fields.Integer("Bedrooms numbers",required=False, default=2)
    living_area = fields.Integer("Living Area",required=False)
    facades = fields.Integer("Facades",required=False)
    garage = fields.Boolean("Garage",required=False)
    garden = fields.Boolean("Garden",required=False)
    garden_area = fields.Integer("garden_area",required=False)
    orientation = fields.Selection(
        string="Garden Orientation",
        selection=[('North','North'),
            ('East','East'),
            ('South','South'),
            ('West','West')]
    )
    estate_state = fields.Selection(
        string="Estate State",
        selection=[('New','New'),
            ('Offer_Received','Offer Received'),
            ('Offer_Accepted','Offer Accepted'),
            ('Sold','Sold'),
            ("Cancelled","Cancelled")],
        default="New",
        copy=False
    )
    active = fields.Boolean("active",required=True,default=True)
    total_area = fields.Float(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer")

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    property_salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    property_buyer_id = fields.Many2one("res.partner", string="Buyer")

    property_tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    property_offer_ids = fields.One2many("estate.property.offer","property_id", string="Offers")

    note = fields.Text("Special mentions about the house.")

    # compute and search fields
    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for prop in self:
            prop.total_area = prop.living_area+prop.garden_area

    @api.depends("property_offer_ids.price")
    def _compute_best_offer(self):
        for prop in self:
            prop.best_offer = max(prop.property_offer_ids.mapped("price")) if prop.property_offer_ids else 0.0

    # Constraints and onchanges# Constraints and onchanges
    @api.constrains("selling_price")
    def _check_selling_price(self):
        for record in self:
            if float_compare(record.selling_price, record.expected_price * 90.0 / 100.0, precision_rounding=0.01) < 0:
                raise ValidationError("The selling price is to low")

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 100
            self.orientation = "North"
        else:
            self.garden_area = 0
            self.orientation = False

    # CRUD methods
    @api.ondelete(at_uninstall=False)
    def _delete_house(self):
        for record in self:
            if record.estate_state not in ["New","Cancelled"]:
                raise UserError("Can't delete an active house!")

    # Action methods
    def action_cancel_property(self):
        for record in self:
            if record.estate_state == "Sold":
                raise UserError('Unable to Cancel a sold estate, please change estate state before continuing.')
            record.estate_state = "Cancelled"
    
    def action_sold_property(self):
        for record in self:
            if record.estate_state == "Cancelled":
                raise UserError('Unable to sold a cancelled estate, please change estate state before continuing.')
            record.estate_state = "Sold"
