from odoo import fields, models, api, exceptions


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=fields.Date.add(fields.Date.today(), months=3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    state = fields.Selection(
        default='new',
        copy=False,
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')])
    active = fields.Boolean(default=True)

    property_type_id = fields.Many2one("estate.property.type", string='Property Type')

    buyer_id = fields.Many2one("res.partner", "Buyer", copy=False)

    salesperson_id = fields.Many2one("res.users", "Salesperson", default=lambda self: self.env.user)

    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    best_offer = fields.Float(compute='_compute_best_offer')

    total_area = fields.Integer(compute='_compute_total_area', string="Total Area (sqm)")

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped(lambda x: 0 if x.status == 'refused' else x.price),
                                    default=0)

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_set_sold_state(self):
        for record in self:
            if record.state == 'cancel':
                raise exceptions.UserError(message="Already a canceled property")
            if record.state == 'sold':
                raise exceptions.UserError(message="Already a sold property")

            record.state = 'sold'
        return True

    def action_set_cancel_state(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError(message="A sold property can't be cancelled")
            if record.state == 'cancelled':
                raise exceptions.UserError(message="Already a cancelled property")

            record.state = 'cancelled'

        return True
