from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available From", copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Float(string="Living Area (spm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Float(string="Garden Area (spm)")
    total_area = fields.Float(string="Total Area (sqm)", compute="_computed_total_area")
    garden_orientation = fields.Selection([
        ('north', "North"),
        ('east', "East"),
        ('west', "West"),
        ('south', "South")
    ])
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection([
        ('new', "New"),
        ('offer_received', "Offer Received"),
        ('offer_accepted', "Offer Accepted"),
        ('sold', "Sold"),
        ('cancelled', "Cancelled")
    ], copy=False, default='new')
    property_type_id = fields.Many2one('estate.property.type', string="Property Type", ondelete="cascade")
    sales_person_id = fields.Many2one('res.users', string='Salesman', ondelete='cascade')
    buyer_id = fields.Many2one('res.partner', string='Buyer', ondelete='cascade')
    property_tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    best_price = fields.Float(string="Best Offer", compute="_computed_best_offer", search="_search_best_offer", store=False)

    @api.depends("living_area", "garden_area")
    def _computed_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends("offer_ids.price")
    def _computed_best_offer(self):
        prices = self.offer_ids.mapped("price")
        self.best_price = max(prices) if prices else 0.0

    def _search_best_offer(self, operator, value):
        return [
            '&',
            ('offer_ids.price', '>', 10000),
            ('offer_ids.price', operator, value)
        ]

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'

            return {
                'warning': {
                    'title': "Garden Enabled",
                    'message': "Default area set to 10 and orientation north",
                    'type': "notification"
                }
            }
        else:
            self.garden_area = 0
            self.garden_orientation = False
