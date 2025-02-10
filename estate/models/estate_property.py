from odoo import models,fields,api
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _name="estate.property"
    _description="Real Estate Property"

    name=fields.Char(required=True)
    description=fields.Text()
    postcode=fields.Char()
    date_availability=fields.Date(
        copy=False,
        default=fields.Date().add(fields.Date().today(),days=90)
    )
    expected_price=fields.Float(required=True)
    selling_price=fields.Float(readonly=True,copy=False)
    bedrooms=fields.Integer(default=2)
    living_area=fields.Float()
    facades=fields.Integer()
    garage=fields.Boolean()
    garden=fields.Boolean()
    garden_area=fields.Float()
    garden_orientation=fields.Selection(selection=[('north','North'),('south','South'),('east','East'),('west','West')])
    active=fields.Boolean("Active",default=True)
    status=fields.Selection(
        selection=[('new','New'),("offer_received","Offer Received"),("offer_accepted","Offer Accepted"),("sold","Sold"),("canceled","Canceled")],
        default='new',copy=False
    )
    property_type_id=fields.Many2one("estate.property.type",string="Property Type")
    buyer_id=fields.Many2one("res.partner",string="Buyer",copy=False)
    salesperson_id=fields.Many2one("res.users",string="Salesperson",default=lambda self:self.env.user)
    tag_ids=fields.Many2many("estate.property.tag")
    offer_ids=fields.One2many("estate.property.offer","property_id")
    total_area=fields.Float(compute="_compute_total_area",string='Total Area')
    best_price=fields.Float(compute="_compute_best_price",string="Best Offer")

    _sql_constraints=[
        ('expected_price_positive','CHECK(expected_price>0)','Expected price must be positive number'),
        ('selling_price_positive','CHECK(selling_price>=0)','Selling price must be positive number')
    ]

    # Computation methods
    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area=record.living_area+record.garden_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            record.best_price=max(record.offer_ids.mapped('price'),default=0)

    #Onchange methods
    @api.onchange('garden')
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area=0.0
            self.garden_orientation=False
        if self.garden:
            self.garden_area=100.0
            self.garden_orientation='north'

    #Action methods
    def action_mark_as_sold(self):
        if self.status=='canceled':
            raise UserError("You cannot sell a canceled property")
        self.write({'status':'sold'})
        return True

    def action_mark_as_cancel(self):
        if self.status=='sold':
            raise UserError("You cannot cancel a sold property")
        self.write({'status':'canceled'})
        return True
