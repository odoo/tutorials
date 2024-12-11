from odoo import api, fields, models
from odoo.tools import date_utils


class RealEstateProperty(models.Model):
    _name = 'real.estate.property'
    _description = "Real Estate Property"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    image = fields.Image(string="Image")
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('under_option', "Under Option"),
            ('sold', "Sold"),
        ],
        required=True,
        default='new',
    )
    type_id = fields.Many2one(
        string="Type", comodel_name='real.estate.property.type', ondelete='restrict', required=True
    )
    selling_price = fields.Float(
        string="Selling Price", help="The selling price excluding taxes.", required=True
    )
    availability_date = fields.Date(string="Availability Date")
    stalled = fields.Boolean(string="Stalled", compute='_compute_stalled', search='_search_stalled')
    floor_area = fields.Integer(
        string="Floor Area", help="The floor area in square meters excluding the garden."
    )
    bedrooms = fields.Integer(string="Number of Bedrooms", default=2)
    has_garage = fields.Boolean(string="Garage")
    has_garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(
        string="Garden Area", help="The garden area excluding the building."
    )
    total_area = fields.Integer(string="Total Area", compute='_compute_total_area', store=True)
    address_id = fields.Many2one(string="Address", comodel_name='res.partner', required=True)
    seller_id = fields.Many2one(string="Seller", comodel_name='res.partner', required=True)
    salesperson_id = fields.Many2one(string="Salesperson", comodel_name='res.users')
    offer_ids = fields.One2many(
        string="Offers", comodel_name='real.estate.offer', inverse_name='property_id'
    )
    is_priority = fields.Boolean(
        string="Priority", compute='_compute_is_priority', search='_search_is_priority'
    )
    best_offer_amount = fields.Float(string="Best Offer", compute='_compute_best_offer_amount')
    tag_ids = fields.Many2many(string="Tags", comodel_name='real.estate.tag')

    @api.depends('availability_date')
    def _compute_stalled(self):
        for property in self:
            property.stalled = property.availability_date < fields.Date.today()

    def _search_stalled(self, operator, value):
        if (operator == '=' and value is True) or (operator == '!=' and value is False):
            return [('availability_date', '<', fields.Date.today())]
        elif (operator == '=' and value is False) or (operator == '!=' and value is True):
            return [('availability_date', '>=', fields.Date.today())]
        else:
            raise NotImplementedError()

    @api.depends('floor_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.floor_area + property.garden_area

    @api.depends('offer_ids.expiry_date')
    def _compute_is_priority(self):
        for property in self:
            is_priority = False
            for offer in property.offer_ids:
                if offer.expiry_date <= fields.Date.today() + date_utils.relativedelta(days=2):
                    is_priority = True
                    break
            property.is_priority = is_priority

    def _search_is_priority(self, operator, value):
        if (operator == '=' and value is True) or (operator == '!=' and value is False):
            return [(
                'offer_ids.expiry_date',
                '<=',
                fields.Date.today() + date_utils.relativedelta(days=2),
            )]
        elif (operator == '=' and value is False) or (operator == '!=' and value is True):
            return [(
                'offer_ids.expiry_date',
                '>',
                fields.Date.today() + date_utils.relativedelta(days=2),
            )]
        else:
            raise NotImplementedError()

    @api.depends('offer_ids.amount')
    def _compute_best_offer_amount(self):
        for property in self:
            if property.offer_ids:
                property.best_offer_amount = max(property.offer_ids.mapped('amount'))
            else:
                property.best_offer_amount = 0
