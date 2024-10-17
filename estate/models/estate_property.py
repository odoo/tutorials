from odoo import models, fields, api # type: ignore
from datetime import timedelta

class estateProperty(models.Model):
        _name = "estate.property"
        _description = "This is property Table."

        name = fields.Char(required=True)
        description = fields.Text()
        postcode = fields.Char()
        data_availability = fields.Date(
            default=lambda self: fields.Date.today() + timedelta(days=90),
            copy=False
        )
        expected_price = fields.Float(required=True)
        selling_price = fields.Float(readonly=True, copy=False)
        bedrooms = fields.Integer(change_default=True)
        living_area = fields.Integer()
        facades = fields.Integer()
        garage = fields.Boolean()
        garden = fields.Boolean()
        garden_area = fields.Integer()
        garden_orientation = fields.Selection(
            string = 'Orientation',
            selection = [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
            help = "Garden Orientation is avialable in four faces of direction."
        )
        active = fields.Boolean(default=True)
        state = fields.Selection(
            string = 'State',
            selection = [('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
            help = "Offer available in five type.",
            required=True,
            copy=False,
            default='new' 
        )
        property_type_id = fields.Many2one(
                comodel_name='estate.property.type',
                string='Property Type',
                domain="[('number', '>=', 0)]",
                ondelete='cascade',
                store=False # 3 option: cascade, set null, restrict
                # index, traking, store, compute, related
        )
        seller_id = fields.Many2one(
                'res.users',
                'Salesman',
                default=lambda self: self.env.user
        )
        buyer_id = fields.Many2one(
                'res.partner',
                'Buyer'
        )
        tag_ids = fields.Many2many(
                comodel_name='estate.property.tag',
                string='Tag',
                relation='property_join_tag',
                column1='property_id',
                column2='tag_id'
        )
        # estate_property_tag_rel automatically made
        offer_ids = fields.One2many(
                'estate.property.offer', 
                'property_id'
        )
        number = fields.Integer(related='property_type_id.number')
        totalArea = fields.Integer(compute='_compute_total_area', store=True)
        percentage_garden = fields.Float(compute='_compute_total_area')
        percentage_living = fields.Float(compute='_compute_total_area')

        best_offer = fields.Float(compute='_compute_best_offer')

        @api.depends('garden_area', 'living_area')
        def _compute_total_area(self):
                self.totalArea = self.garden_area + self.living_area
                # self.percentage_garden = ((self.garden_area) / (self.totalArea)) * 100
                # self.percentage_living = ((self.living_area) / (self.totalArea)) * 100

        @api.depends('offer_ids.price')
        def _compute_best_offer(self):
                # for record in self:
                #         if record.offer_ids:
                #                 prices = [line.price for line in record.offer_ids]
                #                 record.best_offer = max(prices) if prices else 0.0
                #         else:
                #                 record.best_offer = 0.0  # Set to 0 if there are no offers
                for record in self:
                        if record.offer_ids:
                                record.best_offer = max(record.offer_ids.mapped('price'))
                        else:
                                record.best_offer = 0.0

        @api.onchange('garden')
        def _onchange_garden(self):
                if self.garden:
                        self.garden_area = 10
                        self.garden_orientation = 'north'
                else:
                        self.garden_area = 0
                        self.garden_orientation = False


        # offer = fields.Integer(related='offer_ids.id')
        # property_record = self.env['estate.property'].browse(1)
        
