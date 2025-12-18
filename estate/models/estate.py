from odoo import api, fields, models


class Estate(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char("Property Name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From", default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage", default=True)
    garden = fields.Boolean("Garden", default=True)
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[('north', "North"), ('south', "South"), ('east', "East"), ('west', "West")],
        required=True)
    status = fields.Selection(
        string="Status",
        selection=[('new', "New"), ('offer_received', "Offer Received"), ('offer_accepted', "Offer Accepted"), ('sold', "Sold"), ('canceled', "Canceled")],
        default='new',
        required=True)
    active = fields.Boolean("Active", default=True)
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    salesperson_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    total_area = fields.Integer('Total Area (sqm)', compute='_compute_total_area')
    best_price = fields.Float("Best Offer", compute='_compute_best_price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'))

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False
