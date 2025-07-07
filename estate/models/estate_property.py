from odoo import  api,fields,models
from odoo.exceptions import UserError
from datetime import date
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property is defined"

    name= fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_avaiblity = fields.Date(copy=False,default=date.today()+ relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string = 'Direction',
        selection=[('north','North'), ('south','South'), ('east','East'), ('west','West')],
        help = "Orientation is used to locate garden's direction"
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[('new','new'), ('Offer Received','Offer Received'), ('Offer Accepted','Offer Accepted'), ('sold','sold'),('Cancelled','Cancelled')],
        required=True,
        default='new',
        copy=False,
    )
    salesman_id = fields.Many2one("res.users",index=True,string="salesman",default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner",string="buyer",index=True,default=lambda self:self.env.user.partner_id.id)

    property_type_id = fields.Many2one("estate.property.type",string="property type")

    property_tag_ids = fields.Many2many("estate.property.tag",string="tags")

    offer_ids = fields.One2many("estate.property.offer","property_id",string="offers")



    _sql_constraints = [
        ('selling_price_positive','CHECK(selling_price>=0)','The selling price should be positive.'),
        ('expected_price_positive','CHECK(expected_price>=0)','The expected price should be positive.')
    ]

    total_area = fields.Float(compute="_compute_total")

    @api.depends("garden_area","living_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    best_offer = fields.Float(compute="_find_best")

    @api.depends("offer_ids.price")
    def _find_best(self):
        for record in self:
            if record.offer_ids:
               record.best_offer = max(record.offer_ids.mapped('price'))
            else:
                record.best_offer=0.0



    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area=10
            self.garden_orientation="north"
        else:
            self.garden_area = 0
            self.garden_orientation = False


    status = fields.Selection(
        selection=[
            ('new', 'New'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        default='new',
        copy=False
    )

    def sold_button_action(self):
        for record in self:
            if record.status == 'cancelled':
                raise UserError("Cancelled property cannot be marked as sold.")
            record.status = 'sold'

    def cancel_button_action(self):
        for record in self:
            if record.status == 'sold':
                raise UserError("Sold property cannot be cancelled.")
            record.status = 'cancelled'