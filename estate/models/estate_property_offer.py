from odoo import _, api, exceptions, fields, models
from odoo.tools.date_utils import add


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'
    _sql_constraints = [
        ('check_price_strictly_positive', 'CHECK(price > 0)',
         'The price of an offer should be strictly positive.'),
    ]

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
        help="Status of the offer.",
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        required=True,
        help="Partner who made the offer.",
    )
    property_id = fields.Many2one(
        comodel_name='estate.property',
        required=True,
        help="Property for which the offer is made.",
    )
    validity = fields.Integer(
        string="Validity (days)",
        default=7,
        help="Validity period of the offer in days.",
    )
    date_deadline = fields.Date(
        string="Deadline",
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
        store=True,
        help="Deadline for the offer based on validity period.",
    )
    property_type_id = fields.Many2one(
        related='property_id.property_type_id',
    )

    @api.depends('validity')
    def _compute_date_deadline(self):
        for property_offer in self:
            property_offer.date_deadline = add(fields.Date.to_date(property_offer.create_date)
                                               or fields.Date.today(), days=property_offer.validity)

    def _inverse_date_deadline(self):
        for property_offer in self:
            property_offer.validity = (property_offer.date_deadline -
                                       fields.Date.to_date(property_offer.create_date)
                                       or fields.Date.today()).days

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env['estate.property'].browse(vals.get('property_id'))

            if (vals.get('price') < property.best_offer):
                raise exceptions.UserError(
                    _("The offer price must be greater than the best offer of the property.")
                )

            if property.state == 'new':
                property.state = 'offer_received'
        return super().create(vals_list)

    def action_accept(self):
        for property_offer in self:
            if (property_offer.property_id.state != 'offer_accepted'):
                property_offer.status = 'accepted'
                property_offer.property_id.state = 'offer_accepted'
                property_offer.property_id.buyer_id = property_offer.partner_id
                property_offer.property_id.selling_price = property_offer.price

        self.search(
            [('property_id', 'in', property_offer.property_id.ids),
             ('status', '=', False)]
        ).write({'status': 'refused'})

        return True

    def action_refuse(self):
        for property_offer in self:
            property_offer.status = 'refused'
        return True
