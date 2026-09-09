from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Real Estate Property Offer"

    date_deadline = fields.Date(
        string="Deadline",
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline'
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    price = fields.Float()
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    status = fields.Selection(
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ],
        copy=False,
    )
    validity = fields.Integer(string="Validity (days)", default=7)

    _check_offer_price = models.Constraint(
        'CHECK(price > 0)',
        "Offer price must be strictly positive.",
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = fields.Date.add(fields.Date.to_date(create_date), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.validity = (record.date_deadline - fields.Date.to_date(create_date)).days

    def action_accept(self):
        accepted_offer = self.env['estate.property.offer'].search([
            ('property_id', '=', self.property_id.id),
            ('status', '=', 'accepted'),
            ('id', '!=', self.id),
        ], limit=1)

        if accepted_offer:
            raise UserError(
                "Only one offer can be accepted for a property."
            )

        self.status = 'accepted'
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
