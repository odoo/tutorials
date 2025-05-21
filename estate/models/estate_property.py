from odoo import fields, models, api, exceptions

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"

    name = fields.Char('Name', required=True, translate=True)
    description = fields.Text('Description', translate=True)
    postcode = fields.Char('Postcode', translate=True)
    date_availability = fields.Date('Availability')
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('Selling price', readonly=True)
    bedrooms = fields.Integer('Bedrooms', required=True, default=2)
    living_area = fields.Integer('Living Areas', required=True)
    facades = fields.Integer('Facades', required=True)
    garage = fields.Boolean('Has a garage')
    garden = fields.Boolean('Has a garden')
    garden_area = fields.Integer('m² of garden area')
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('east', 'East'), ('west', 'West'), ('south', 'South')],
        help="Orientation is used to tell which way the garden is, relative to the house"
    )
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float("Best Offer", compute="_compute_best_price")

    # Reserved Fields
    active = fields.Boolean()
    state = fields.Selection(
        string='Status',
        selection=[('new', 'New'), ('received', 'Offer received'), ('accepted', 'Offer accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        default='new'
    )

    # Foreign keys
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price") # Still computed even without offers
    def _compute_best_price(self):
        for record in self:
            prices = record.mapped("offer_ids.price")
            record.best_price = max(prices, default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            record.garden_area = 10 if record.garden else None
            record.garden_orientation = "north" if record.garden else None

    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise exceptions.UserError("Canceled properties cannot be sold.")

            record.state = "sold";
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise exceptions.UserError("Sold properties cannot be canceled.")

            record.state = "canceled";
        return True

