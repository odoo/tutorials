from odoo import api, fields, models, exceptions, tools
from dateutil.relativedelta import relativedelta

class Estate_property(models.Model):
    _name = "estate.property"
    _description = "Model to modelize Real Estate objects"
    _order= "id desc"

    name = fields.Char(string="Name", required=True)
    description  = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Datetime(copy=False, default=fields.date.today() + relativedelta(months=3))
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
        selection=[('north','North'), ('south','South'),('east','East'),('west','West')],
        help="Orientation is meant to describe the garden."
    )
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string='Status',
        selection=[('new','New'), ('offer_received','Offer Received'),('offer_accepted','Offer Accepted'),('sold','Sold'),('cancelled', 'Cancelled')],
        help="State is meant to describe the evolution.",
        default='new',
        copy=False
    )
    buyer_id = fields.Many2one("res.partner")
    seller_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    property_type_id = fields.Many2one("estate.property.type")
    property_tag_ids = fields.Many2many("estate.property.tags")
    property_offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_area")
    best_offer_price = fields.Float(compute="_compute_best_offer")

    _sql_constraints = [
        ('positive_expected_price', 'CHECK(expected_price >=0)', 'The Property\'s expected price must be positive.'),
        ('positive_selling_price', 'CHECK(selling_price >=0)', 'The Property\'s selling price must be positive.')
    ]

    @api.depends("garden_area", "living_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("property_offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer_price = max(p.price for p in record.property_offer_ids) if record.property_offer_ids else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        print("entered")
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = "north" if self.garden else None

    def sell_property(self):
        for record in self:
            if(record.state == "cancelled"):
                raise exceptions.UserError("A Cancelled Property can't be sold")
            record.state = "sold"
        return True

    def cancel_property(self):
        for record in self:
            if(record.state == "sold"):
                raise exceptions.UserError("A Sold Property can't be cancelled")
            record.state = "cancelled"
        return True

    def has_accepted_offer(self):
        for record in self:
            if(list(filter(lambda offer: offer.status == "accepted", record.property_offer_ids))):
                return True
        return False

    @api.onchange("expected_price")
    def _onchange_expected_price(self):
        if(self.has_accepted_offer()):
            compute_cost = self.expected_price *90/100
            print(compute_cost)
            if(tools.float_utils.float_compare(compute_cost, self.selling_price, 2) > 0):
                raise exceptions.ValidationError("The selling price must be equal or higher than 90% of the selling price.")

    @api.model
    def ondelete(self):
        print("deletion")
        for record in self:
            if(not record.state in ['new','cancelled']):
                raise exceptions.UserError("Only new or cancelled Property can be deleted.")
        return super().ondelete()