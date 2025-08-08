from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class estateProperty(models.Model):
        _name = "estate.property"
        _description = "This is property Table."
        _order = "selling_price desc, name"

        name = fields.Char(required=True)
        description = fields.Text()
        postcode = fields.Char()
        data_availability = fields.Date(default=lambda self: fields.Date.today() + timedelta(days=90), copy=False)
        expected_price = fields.Float(required=True)
        selling_price = fields.Float(readonly=True, copy=False)
        bedrooms = fields.Integer(change_default=True)
        living_area = fields.Integer()
        facades = fields.Integer()
        garage = fields.Boolean()
        garden = fields.Boolean()
        garden_area = fields.Integer()
        garden_orientation = fields.Selection(
            string='Orientation',
            selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
            help="Garden Orientation is avialable in four faces of direction."
        )
        active = fields.Boolean(default=True)
        state = fields.Selection(
            string='State',
            selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
            help="Offer available in five type.",
            required=True,
            copy=False,
            default='new'
        )
        number = fields.Integer(related='property_type_id.number')
        totalArea = fields.Integer(compute='_compute_total_area', store="true")
        best_offer = fields.Float(compute='_compute_best_offer')
        property_image = fields.Binary()

        property_type_id = fields.Many2one(comodel_name='estate.property.type', string='Property Type', domain="[('number', '>=', 0)]", ondelete='cascade')
        seller_id = fields.Many2one('res.users', 'Salesman', default=lambda self: self.env.user)
        buyer_id = fields.Many2one('res.partner', 'Buyer')
        tag_ids = fields.Many2many(comodel_name='estate.property.tag', string='Tag', relation='property_join_tag', column1='property_id', column2='tag_id')
        offer_ids = fields.One2many('estate.property.offer', 'property_id')
        company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)


        _sql_constraints = [
                ('check_selling_price', 'CHECK(selling_price >= 0)', 'A property selling price must be positive.'), 
                ('check_expected_price', 'CHECK(expected_price > 0)', 'A property expected price must be strictly positive.')
        ]

        @api.depends('garden_area', 'living_area')
        def _compute_total_area(self):
                for record in self:
                        record.totalArea = record.garden_area + record.living_area

        @api.depends('offer_ids.price')
        def _compute_best_offer(self):
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

        def action_sold(self):
                if(self.state == 'cancelled'):
                        raise UserError("You can not mark a cancelled property as sold.")
                self.state = 'sold'
        
        def action_cancelled(self):
                if(self.state == 'sold'):
                        raise UserError("You can not mark sold property as cancelled")
                self.state = 'cancelled'

        @api.constrains('selling_price', 'expected_price')
        def _check_selling_price(self):
                for record in self:
                        if record.selling_price < (0.9 * record.expected_price) and (record.selling_price > 0):
                               raise ValidationError("Selling price cannot be lower than 90 percentage of the expected price.")

        @api.ondelete(at_uninstall=False)
        def _prevent_delete(self):
                for record in self:
                        if record.state not in ("new", "cancelled"):
                                raise UserError("You can not delete a property which are in offer received, offer accepted or sold state.")
