from odoo import api, fields, models


class RecurringPlan(models.Model):
    _name = "estate.property"
    _description = "Real estate"

    name = fields.Char(required=True, string='Title')
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Datetime(string='Available From',
                                        copy=False,
                                        default=fields.Date.add(fields.Date.today(), months=3))

    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson",
                                        default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden orientation',
        selection=[('north', 'North'), ('east', 'East'),
                   ('south', 'South'), ('west', 'West')],
        help="Type is used to separate Leads and Opportunities")

    # Computed fields
    total_area = fields.Integer(compute="_compute_total_area")
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_price = fields.Float(compute="_find_best_price")
    @api.depends("offer_ids", "offer_ids.price")
    def _find_best_price(self):
        for record in self:
            best_price = float('inf')
            for offer in self.offer_ids:
                best_price = min(best_price, offer.price)
            if best_price == float('inf'):      best_price = 0
            record.best_price = best_price

    # Reserved fields
    active = fields.Boolean(default=True)
    state = fields.Selection(
        default='new', required=True, copy=False,
        selection=[('new', 'New'), ('received', 'Offer Received'),
                    ('accepted', 'Offer Accepted'), ('sold', 'Sold'),
                    ('cancelled', 'Cancelled')])
