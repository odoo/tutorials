from odoo import api, exceptions, fields ,models
from datetime import date , timedelta
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare , float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property" 
    _description = "Real Estate Property"
    _order = "id desc" 

    name = fields.Char(string="Title", required=True)
    expected_price = fields.Float(string="Expected Price", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From",copy=False,default=lambda self: date.today() + timedelta(days=(90)))
    selling_price = fields.Float(string="Selling Price",readonly=True,copy=False)
    bedrooms = fields.Integer(string="Bedrooms",default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    active = fields.Boolean(default=True)
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
                                [('north', 'North'), 
                                ('south', 'South'),
                                ('east', 'East'), 
                                ('west', 'West')],
                                string="Garden Orientation")

    state = fields.Selection([
                        ('new', 'New'),
                        ('offer_received','Offer Received'),
                        ('offer_accepted', 'Offer Accepted'),
                        ('sold', 'Sold'),
                        ('cancelled', 'Cancelled'),
                        ],
                        string="State",
                        required=True,
                        default='new',
                        copy=False)
    
    # many2one
    property_type_id = fields.Many2one("estate.property.type",string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users",string="Salesman",default=lambda self: self.env.user)
    
    #many2one 
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    #one2many
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    # total Area
    total_area = fields.Float(compute="_compute_total_area", store=True , string="Total Area")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    # best_price
    best_offer = fields.Float(compute="_compute_best_offer", store=True)

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            # Using mapped() to get all offer prices and then find the maximum
            record.best_offer = max(record.offer_ids.mapped("price"), default=0.0)

    
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_set_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise exceptions.UserError("A canceled property cannot be sold!")
            record.state = "sold"
        return True

    def action_cancel_property(self):
        for record in self:
            if record.state == "sold":
                raise exceptions.UserError("A sold property cannot be canceled!")
                record.state = "cancelled"
        return True

    def action_accept_offer(self):
        for record in self:
            if record.property_id.state == "sold":
                raise exceptions.UserError("You cannot accept an offer for a sold property!")
            record.status = "accepted"
            record.property_id.write({
                'state': 'sold',
                'buyer_id': record.buyer_id.id,
                'selling_price': record.price
                })
        return True

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 
         'The expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 
         'The selling price must be positive.')
    ]

    # @api.constrains('selling_price', 'expected_price')
    # def _check_selling_price(self):
    #     for record in self:
    #         if record.selling_price > 0 and record.selling_price < record.expected_price * 0.9:
    #             raise ValidationError(f"The selling price cannot be lower than 90% of the expected price.")


    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, 
                                precision_digits=2):
                if float_compare(record.selling_price, 
                                record.expected_price * 0.9, 
                                precision_digits=2) < 0:

                    raise ValidationError(
                        f"The selling price cannot be lower than 90% of the expected price.")


    # @api.model
    # def unlink(self):
    #     for property in self:
    #         if property.state not in ['New', 'Cancelled']:
    #             raise ValidationError("You cannot delete a property unless its state is 'New' or 'Cancelled'.")
    #     return super(Property, self).unlink()

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        for record in self:
            if record.state not in ('new', 'cancelled'):
                raise exceptions.UserError(
                    "You can only delete properties in 'New' or 'Cancelled' state."
                    )