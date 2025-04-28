from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    # ------------------
    # Private attributes
    # ------------------

    _name = "estate.property.offer"
    _description = "This class allows to manage offers for a property."
    _order = "price desc"
    _sql_constraints = [
        ('offer_price_constraint', 'CHECK(price > 0)',
         'Your price offer must be positive.')
    ]

    # ---------------
    # Default methods
    # ---------------

    def _default_creation_date(self):
        return fields.Date.today()

    # ------------------
    # Field declarations
    # ------------------

    price = fields.Float()
    status = fields.Selection(copy=False,
                              selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    creation_date = fields.Date(readonly=True, default=lambda self: self._default_creation_date())  # To fix the creation date
    validity = fields.Integer(string="Validity (days)", default=7)  # Default validity days
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    # Many2One relationships
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    property_type_id = fields.Many2one('estate.property.type', related="property_id.property_type_id", store=True)

    # ---------------------------
    # Compute and inverse methods
    # ---------------------------

    @api.depends('creation_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.creation_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.creation_date).days

    # ------------
    # CRUD methods
    # ------------

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            property_onchange = self.env['estate.property'].browse(val['property_id'])

            if val.get("price", 0) < property_onchange.best_price:
                raise ValidationError("Your offer is under the best offer.")

            property_onchange.state = 'offer_received'
        return super().create(vals_list)

    # --------------
    # Action methods
    # --------------

    def action_accept_offer(self):
        self.ensure_one()
        for record in self:
            if not record.status:
                property_from_offer = record.property_id
                # Refuse all the other offers
                for offer in property_from_offer.offer_ids:
                    offer.status = "refused"

                record.status = "accepted"
                property_from_offer.state = "offer_accepted"
                property_from_offer.selling_price = record.price
                property_from_offer.buyer_id = record.partner_id
        return True

    def action_refuse_offer(self):
        self.ensure_one()
        for record in self:
            if not record.status:
                record.status = "refused"
        return True
