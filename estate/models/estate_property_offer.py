from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'
    _order= 'price desc'

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused")
        ],
        copy=False
    )
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline'
    )
    partner_id = fields.Many2one(string="Partner", comodel_name='res.partner', required=True)
    property_id = fields.Many2one(string="Property", comodel_name='estate.property', required=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    _sql_constraints = [
        ('unique_partner_offer', 'unique(partner_id, property_id)', "A partner can only make one offer per property.")
    ]

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for offer in self:
            base_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = base_date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            base_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - base_date).days

    def action_confirm(self):
        """Confirm the offer and refuse all other offers."""
        self.ensure_one()
         # Refuse all other offers related to the same property
        other_offers = self.env['estate.property.offer'].search([
            ('property_id', '=', self.property_id.id),
            ('id', '!=', self.id)  # Exclude the current offer
        ])
        other_offers.write({'status': 'refused'})
        self.write({'status': 'accepted'})
        self.property_id.write({
            'state': 'offer_accepted',
            'selling_price': self.price,
            'buyer_id': self.partner_id.id
        })

    def action_cancel(self):
        """Cancel the offer by setting its status to refused."""
        self.ensure_one()
        self.status = 'refused'

    @api.model_create_multi
    def create(self, vals_list):
        """Overrides the create method to enforce business rules on multiple offers."""
        for vals in vals_list:
            if vals['property_id']:
                property = self.env['estate.property'].browse(vals['property_id'])
                if property.best_price >= vals['price']:
                    raise ValidationError(
                        "You cannot create an offer lower than or equal to an existing offer for this property."
                    )
                if property.state in ['sold', 'cancelled', 'offer_accepted']:
                    raise ValidationError(
                        f"You can not create offer for property state in {property.state}"
                    )
                elif property.state == 'new':
                    property.write({'state': 'offer_received'})
        return super().create(vals_list)
