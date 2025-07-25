from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import _, api, exceptions, fields, models
from odoo.tools import float_utils


class EstatePropertyOffer(models.Model):
    # ----------------------------------------
    # Private attributes
    # ----------------------------------------
    _name = 'estate.property.offer'
    _description = "Offers for estate properties."
    _sql_constraints = [
        (
            'check_offer_price_positive',
            'CHECK (price > 0)',
            "Offer price must be positive.",
        )
    ]
    _order = 'price desc'

    # ----------------------------------------
    # Field declarations
    # ----------------------------------------
    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[('accepted', "Accepted"), ('refused', "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one(
        'res.partner', string="Buyer", index=True, required=True
    )
    property_id = fields.Many2one(
        'estate.property',
        string="Property",
        index=True,
        required=True,
        ondelete='cascade',
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date()

    # ----------------------------------------
    # Constrains and onchange methods
    # ----------------------------------------
    @api.onchange('validity')
    def _onchange_validity(self):
        base_date = (self.create_date or date.today()).days()
        self.date_deadline = base_date + relativedelta(days=self.validity)

    @api.onchange('date_deadline')
    def _onchange_date_deadline(self):
        if self.date_deadline:
            base_date = (
                self.create_date.date() if self.create_date else date.today()
            )
            self.validity = (self.date_deadline - base_date).days

    # ----------------------------------------
    # CRUD methods (ORM overrides)
    # ----------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        # Check price validation before creating offers
        for vals in vals_list:
            if 'property_id' in vals and 'price' in vals:
                property_obj = self.env['estate.property'].browse(
                    vals['property_id']
                )
                if (
                    property_obj.best_price > 0
                    and float_utils.float_compare(
                        vals['price'],
                        property_obj.best_price,
                        precision_digits=2
                    ) <= 0
                ):
                    raise exceptions.ValidationError(
                        _(
                            "Offer price (%(price)s) must be greater than the property's best price (%(best_price)s).",
                            price=vals['price'],
                            best_price=property_obj.best_price,
                        )
                    )

        offers = super().create(vals_list)
        # Update property state to 'offer_received' when an offer is created
        for offer in offers:
            if offer.property_id and offer.property_id.state == 'new':
                offer.property_id.state = 'offer_received'
        return offers

    # ----------------------------------------
    # Action methods
    # ----------------------------------------
    def action_confirm_offer(self):
        for offer in self:
            # Refuse all other offers for this property
            (offer.property_id.offer_ids - self).write({'status': 'refused'})

            # Accept this offer
            offer.property_id.state = 'offer_accepted'
            offer.property_id.selling_price = offer.price
            offer.status = 'accepted'

    def action_cancel_offer(self):
        for offer in self:
            offer.status = 'refused'
