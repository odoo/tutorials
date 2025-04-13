import datetime

from odoo import models, fields, api


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _order = 'name desc'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date('Available From',
                                    default=fields.Datetime.today() + datetime.timedelta(
                                        days=90))
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    bathrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean(default=False)
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    temp = fields.Char()
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer received', 'Offer Received'),
        ('offer accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ], required=True, default='new', copy=False)
    property_type_id = fields.Many2one('estate.property.type',
                                       string='Property Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    salesperson_id = fields.Many2one('res.users', string='Salesman',
                                     default=lambda self: self.env.user)
    tags_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Integer(string='Total Area(sqm)',
                                compute='_compute_total_area')
    best_price = fields.Float(string='Best Price',
                              compute='_compute_best_price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    def _compute_best_price(self):
        for record in self:
            record.best_price = max(
                record.offer_ids.mapped('price')) if record.offer_ids else 0.0


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    name = fields.Char(required=True)


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    property_id = fields.Many2one('estate.property', required=True)
    partner_id = fields.Many2one('res.partner', required=True)
    price = fields.Float()
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], copy=False)
    validity = fields.Integer(default=7)
    date_deadline = fields.Datetime('Deadline',
                                    compute='_compute_date_deadline',
                                    inverse='_inverse_date_deadline',
                                    store=True)

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        """Вычисляет дату окончания на основе даты создания и срока действия"""
        for record in self:
            if record.create_date:
                print(f'create_date: {record.create_date}')
                record.date_deadline = record.create_date + datetime.timedelta(
                    days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + datetime.timedelta(
                    days=record.validity)

    def _inverse_date_deadline(self):
        """Обратное вычисление - позволяет установить срок действия через изменение даты окончания"""
        for offer in self:
            if offer.create_date and offer.date_deadline:
                create_date = fields.Date.from_string(offer.create_date)
                deadline_date = fields.Date.from_string(offer.date_deadline)
                # Вычисляем разницу в днях между датой создания и крайним сроком
                offer.validity = (deadline_date - create_date).days
