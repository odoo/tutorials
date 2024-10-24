from datetime import timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Model representing the offers from partners to a specific property'
    _order = 'price desc'

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused")
        ]
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline', string="Date Deadline")
    create_date = fields.Date(default=lambda self: fields.Datetime.now())
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)',
         "The offer price should be greater than 0."),
    ]

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            delta = record.date_deadline - record.create_date

            record.validity = delta.days

    def action_confirm(self):
        self.ensure_one()

        if self.status == 'accepted':
            raise UserError(_("Offer already accepted!"))
        elif self.status == 'refused':
            raise UserError(_("Can't accept a refused offer!"))
        elif self.property_id.buyer_id:
            raise UserError(_("Can't accept more than 1 offer!"))
        else:
            if float_compare(self.price, 0.9 * self.property_id.expected_price, 5) == -1:
                raise UserError(_("Selling price cannot be lower than 90% of the expected price!"))

            self.status = 'accepted'
            self.property_id.state = 'offer_accepted'
            self.property_id.selling_price = self.price
            self.property_id.buyer_id = self.partner_id

        return True

    def action_refuse(self):
        for record in self:
            if record.status == 'refused':
                raise UserError(_("Offer already refused!"))
            elif record.status == 'accepted':
                raise UserError(_("Can't refuse an accepted offer!"))
            else:
                record.status = 'refused'

        return True
