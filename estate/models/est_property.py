from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero
from odoo._ import _

class EstateProperty(models.Model):
    _name = "est.property"
    _description = "Real Estate"
    _order = "id desc"

    _check_expected_price = models.Constraint(
        'CHECK (expected_price >= 0)',
        'The Expected Price should be positive!',
    )

    _check_selling_price = models.Constraint(
        'CHECK (selling_price >= 0)',
        'The Selling Price should be positive!',
    )
    def _today_plus_90days(self):
        return fields.Date.today(self) + timedelta(days=90)
    
    name = fields.Char('Property Name', required=True)
    description = fields.Text(required=True)
    post_code = fields.Char(required=True)
    date_availability = fields.Date(default=(_today_plus_90days)) #add 90 days which is about 3 months
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[("north","North"),("south","South"),("east","East"),("west","West")])
    active = fields.Boolean("Active",default=True)
    state = fields.Selection(
        selection = [("new","New"),("offer_received","Offer Received"),("offer_accepted","Offer Accepted"),("sold","Sold"),("cancelled","Cancelled")],
        default = "new"
    )
    partner_id = fields.Many2one("res.partner", string="Buyer")
    user_id = fields.Many2one("res.users", string="Salesman")
    property_type_id = fields.Many2one("est.property.type", string="Property Type")
    
    tag_ids = fields.Many2many("est.property.tag",string="Tags")

    offers_ids = fields.One2many("est.property.offer","property_id",string="Offers")

    total_area = fields.Integer(compute="_compute_total", readonly=True)
    max_offer = fields.Integer(compute="_compute_best_offer", readonly=True)
    
    @api.constrains("selling_price")
    def _check_selling_price(self):
        for property in self:
            ## if different than 0 and selling_price < 90% of expected_price
            if  (not float_is_zero(self.selling_price,precision_digits=3) and (1 == float_compare(self.expected_price * .9, self.selling_price, precision_digits=3))):  
                raise ValidationError(r"Selling price can't be less than 90% expected price")


    @api.depends("living_area","garden_area")
    def _compute_total(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offers_ids")
    def _compute_best_offer(self):
        
        for property in self:
            property.max_offer = max(property.offers_ids.mapped("price"),default=0)
            
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.ondelete(at_uninstall=False)
    def _ondelete(self):
        for property in self:
            if not(property.state == "new" or property.state == "cancelled"):
                raise UserError(_("You can only delete properties that are 'New' or 'Cancelled'."))

    # ------------- Actions -------------------------------

    def sell_action(self):
        for property in self:
            if self.state == "cancelled":
                #Raise error
                raise UserError(_("Can't change to Sold if current state is Cancelled!"))
            else:
                self.state = "sold"

    def cancel_action(self):
        for property in self:
            if self.state =="sold":
                #Raise error
                raise UserError(_("Can't change to Cancel if current state is Sold!"))
            else:
                self.state = "cancelled"
