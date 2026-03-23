from odoo import models, fields, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Char(required=True)
    status = fields.Selection(
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ],
        copy=False,
    )

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
    )

    partner_id = fields.Many2one(comodel_name='res.partner', string="Partner")
    property_id = fields.Many2one(comodel_name='estate.property', string="Property")
    property_type_id = fields.Many2one(
        comodel_name='estate.property.type',
        related='property_id.property_type_id',
        string="Property Type",
        store=True
    )

    _check_price = models.Constraint(
        'CHECK(price > 0', "The offer price must be strictly positive."
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            date_start = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(date_start, days=record.validity)

    @api.model_create_multi
    def create(self, vals_list):
        property_ids = [v.get('property_id') for v in vals_list if v.get('property_id')]
        properties = self.env['estate.property'].browse(property_ids)
        property_map = {p.id: p for p in properties}

        for vals in vals_list:
            prop_id = vals.get('property_id')
            property_rec = property_map.get(prop_id)

            if property_rec and property_rec.offer_ids:
                max_offer = max(property_rec.offer_ids.mapped('price'))
                if vals.get('price', 0) < max_offer:
                    raise UserError(f"You cannot make an offer lower ({vals.get('price', 0)}) than the current highest offer ({max_offer}).")

        return super().create(vals_list)

    def _inverse_date_deadline(self):
        for record in self:
            date_start = record.create_date.date() if record.create_date else fields.Date.today()

            if record.date_deadline:
                record.validity = (record.date_deadline - date_start).days
            else:
                record.validity = 7

    def action_accept(self):
        for record in self:
            if record.property_id.state == 'offer_accepted':
                raise UserError("An offer has already been accepted for this property!")

            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'offer_accepted'

        return True

    def action_refuse(self):
        for record in self:
            if record.property_id.state == 'sold':
                raise UserError("The property has been already sold !")

            record.status = 'refused'

        return True
