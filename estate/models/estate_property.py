from odoo import api, fields, models, exceptions, tools

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate property descripction"
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price>0)', 
         'The expected price is stricly positive'),
        ('check_selling_price', 'CHECK(selling_price>0)',
         'The selling price is stricly positive'),
    ]
    _order = 'id desc'

    name = fields.Char(required=True, string="Name")
    description = fields.Text(string="description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Availability Date", copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True, string="Expected Price")
    selling_price = fields.Float(readonly=True, copy=False, string="Selling Price")
    bedrooms = fields.Integer(default=2, string="Bedrooms")
    living_area = fields.Integer(string="Living Area")
    facedes = fields.Integer(string="Facedes")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    active = fields.Boolean(default=True, string="Active")
    state = fields.Selection(selection=[
        ('new', 'New'),
        ('offer received', 'Offer Received'),
        ('offer accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')],
        default='new', string='State', copy=False, required=True
    )
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    sale_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.uid)
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    tag_ids = fields.Many2many('estate.property.tag', string="Tag")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    # ---------- CONSTRAIN FUN

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if tools.float_utils.float_compare(record.selling_price, record.expected_price * 0.1, precision_digits=2) < 0:
                raise exceptions.ValidationError("Selling price inferior than 90% of expected price")

    @api.ondelete(at_uninstall=False)
    def _unlink_except_state_not_new_cancelled(self):
        if self.state != 'new' or self.state != 'cancelled':
            raise exceptions.UserError("Delete a property only if state is new or cancelled")

    # --------- COMPUTE FUN

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            if record.mapped('offer_ids.price'):
                record.best_price = max(record.mapped('offer_ids.price'))
            else:
                record.best_price = 0

    # --------- ONCHANGE FUN

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    # --------- ACTION FUN

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError("Sold property cannot be cancelled")
            else:
                record.state = 'cancelled'
        return True

    def hello_daye(self):
        print("I'm a conflict in your branch")

    # ---------- CONSTRAIN FUN

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise exceptions.UserError("Cancelled property cannot be sold")
            else:
                record.state = 'sold'
        return True
