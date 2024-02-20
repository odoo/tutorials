from odoo import fields, models, api


class Estate(models.Model):
    _name = "estate.property"
    _description = "Properties of estate entities."

    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)

    salesperson = fields.Many2one(
            "res.users",
            string="Salesperson",
            default=lambda self: self.env.user)

    offer_ids = fields.One2many(
            "estate.property.offer", "property_id", string="Offer")

    best_price = fields.Float(compute="_getMaxOffer", string="Best Price")

    active = fields.Boolean(default=True)

    name = fields.Char(string="Name", required=True)

    description = fields.Text()

    property_type_id = fields.Many2one("estate.property.type", string="Type")

    postcode = fields.Char()

    date_availability = fields.Date(
            copy=False,
            default=fields.Date.add(fields.Date.today(), months=3))

    expected_price = fields.Float(required=True, readonly=True, default=99999)

    selling_price = fields.Float(copy=False, readonly=True)

    bedrooms = fields.Integer(default=2)

    living_area = fields.Integer()

    facades = fields.Integer()

    garage = fields.Boolean()

    garden = fields.Boolean()

    garden_area = fields.Integer()

    garden_orientation = fields.Selection(
            string='Orientation',
            selection=[
                ('north', 'North'),
                ('south', 'South'),
                ('east', 'East'),
                ('west', 'West')],
            help="Cardinal orientation of the garden.",)

    state = fields.Selection(
            string='State',
            required=True,
            copy=False,
            default='new',
            selection=[
                ('new', 'New'),
                ('offer received', 'Offer Received'),
                ('offer accepted', 'Offer Accepted'),
                ('sold', 'Sold'),
                ('canceled', 'Canceled')])

    total_area = fields.Integer(
            string="Total Area",
            compute="_compute_total")

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids")
    def _getMaxOffer(self):
        for record in self:
            offers = self.offer_ids.mapped("price")
            max = 0
            for offer in offers:
                if offer > max:
                    max = offer
        record.best_price = max
