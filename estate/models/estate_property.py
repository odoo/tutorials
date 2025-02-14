from odoo import api,fields,models, _
from odoo.exceptions import UserError,ValidationError
from odoo.tools.float_utils import float_compare

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "See properties"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default= lambda self:fields.Date.add(fields.Date.today(), months=3),copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Type',
        selection=[('north','North'),
                ('east','East'),
                ('west','West'),
                ('south','South')]
    )
    active = fields.Boolean(default="True")
    state = fields.Selection(
        selection=[('new','New'), 
                   ('offer_recieved','Offer Recieved'), 
                   ('offer_accepted','Offer Accepted'), 
                   ('sold','Sold'),
                   ('cancelled','Cancelled')],
        required=True,
        copy=False,
        default='new'
    )

    property_type_id = fields.Many2one("estate.property.type", string="Property Types")
    buyer_id = fields.Many2one("res.partner", string="seller")
    seller_id = fields.Many2one("res.users", string="buyer", default=lambda self: self.env.user)
    property_tag_ids = fields.Many2many("estate.property.tags", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer","property_id", string="Offers")
    company_id = fields.Many2one("res.company",string="Company", default=lambda self: self.env.company)

    total_area = fields.Float(compute="_compute_total_area",store=True)
    best_price = fields.Float(compute="_compute_best_price",store=True)

    _sql_constraints = [
        ('check_pos_expected_price','CHECK(expected_price > 0)','Expected price shall be greater than 0.'),
        ('check_pos_selling_price','CHECK(expected_price >= 0)','Price cannot be negative')
    ]

    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold_property(self):
        if self.state!='cancelled':
            if self.state=='offer_accepted':
                self.state = 'sold'
            else:
                raise UserError("Accept a offer first.")
        else:
            raise UserError("Cancelled Properties cannot be sold.")
        return True

    def action_cancel_property(self):
        self.state = 'cancelled'
        self.selling_price = False
        return True

    @api.constrains('selling_price','expected_price')
    def _check_selling_price_gt_90(self):
        for record in self:
            if record.selling_price > 0:
                if float_compare(record.selling_price,0.9*record.expected_price,precision_digits=2)<0:
                    raise ValidationError("The selling price cannot be lower than 90 percentage of the expected price. You must lower your expected price or increase offered price.")

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_cancelled(self):
        for record in self:
            if record.state not in ['new','cancelled']:
                raise UserError("Only new and cancelled properties can be deleted!")
        return True
    