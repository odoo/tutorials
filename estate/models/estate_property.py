from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.date_utils import relativedelta
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate model"
    _order = "id desc"

    _sql_constraints = [
        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'The selling price must be positive'),
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The expected price must be strictly positive')
    ]



    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda _: fields.Datetime.today() + relativedelta(month=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()

    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
            string="state",
            selection=[('new', 'New'), ('received', 'Offer Received'), ('accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
            default="new"
    )
    
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one("res.users", string="Salesperson")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    property_tags_ids = fields.Many2many("estate.property.tag", string="Property Categories")
    offer_ids = fields.One2many("estate.property.offer", string="Offers", inverse_name="property_id")

    total_area = fields.Integer(compute="_compute_total_area")
    best_offer = fields.Integer(compute="_compute_best_offer")

    # Compute functions
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price'), default=0) 

    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = "north" if self.garden else ""

    # Actions
    def action_set_state_sold(self):
        self.ensure_one()

        accepted_offers = self.offer_ids.filtered(lambda offer: offer.status == "accepted")
        if len(accepted_offers) == 0:
            raise UserError(_("Cannot sell a property with no accepted offers"))

        if self.state == "cancelled": 
            raise UserError(_("Cannot sell a cancelled property"))
        
        self.state = "sold"

        return True

    def action_set_state_cancelled(self):
        self.ensure_one()


        if self.state == "sold": 
            raise UserError(_("Cannot cancel a sold property"))

        self.state = "cancelled"

        return True

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        self.ensure_one()


        if(float_is_zero(self.selling_price, precision_digits=4)):
            return

        if(float_compare(self.selling_price, self.expected_price * 0.9, precision_digits=4) < 0):
            raise ValidationError(_("The selling price must be at least 90% of the expected price"))

    @api.ondelete(at_uninstall=False)
    def _unlink_if_not_new_or_cancelled(self):
        if self.filtered(lambda rec: rec.state in ('received', 'accepted', 'sold')):
            raise UserError(_("Cannot delete a property which is not in new or cancelled state"))
    

