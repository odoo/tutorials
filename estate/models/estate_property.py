from odoo import api, fields, models, exceptions
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Real estate property"
    _order = "id desc"

    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "The expected price must be strictly positive"),
        ("check_selling_price", "CHECK(selling_price >= 0)", "The offer price must be positive"),
    ]

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date("Available From", copy=False, default=fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[('new', 'New'), ('offer-received', 'Offer Received'), ('offer-accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        copy=False, default="new", required=True)
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False, readonly=True)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")
    
    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    
    @api.depends("offer_ids")
    def _compute_best_price(self):
        for prop in self:
            prop.best_price = max((offer.price for offer in prop.offer_ids), default=0)

    
    @api.onchange("garden")
    def _onchange_garden(self):
        if(self.garden):
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

        
    def sell_property(self):
        for prop in self:
            if(prop.state == 'sold'):
                continue
            elif(prop.state == 'cancelled'):
                raise exceptions.UserError('Cannot sell a cancelled property')
            elif(prop.state != 'offer-accepted'):
                raise exceptions.UserError('Cannot sell a property with no accepted offer')
            else:
                prop.state = 'sold'
            return True

    def cancel_property(self):
        for prop in self:
            if(prop.state == 'cancelled'):
                continue
            elif(prop.state == 'sold'):
                raise exceptions.UserError('Cannot cancel a sold property')
            else:
                prop.state = 'cancelled'
            return True


    @api.constrains("selling_price", "expected_price")
    def _check_price(self):
        for prop in self:
            if(not(prop.selling_price is None or float_is_zero(prop.selling_price, precision_digits=2)) and \
                float_compare(prop.selling_price, prop.expected_price * 9 / 10, precision_digits=2) < 0):
                raise exceptions.ValidationError("The selling price cannot be below 90 percent of the expected price")

    
    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled_(self):
        if any(prop.state != 'new' and prop.state != 'cancelled' for r in self):
            raise exceptions.UserError("Can only delete new or cancelled properties")

