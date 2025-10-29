from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"
    _check_price = models.Constraint("CHECK(price>0)", "Le prix doit être strictement positif.")

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[('Accepted', 'Accepted'), ('Refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.create_date or fields.Date.today(), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.to_date(record.create_date)).days

    def action_accept(self):
        self.ensure_one()
        if float_compare(self.price, self.property_id.best_price, 2) == -1:
            raise ValidationError(_("Cette offre ne peut pas être acceptée car son montant est inférieur à %d", self.property_id.best_price))
        self.status = "Accepted"
        self.property_id.state = "Offer Accepted"
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price
        return True

    def action_refuse(self):
        self.ensure_one()
        self.status = "Refused"
        return True

    @api.constrains("price")
    def _check_offer_price_is_ok(self):
        for record in self:
            if float_compare(record.price, record.property_id.best_price, 2) == -1:
                raise ValidationError(_("Le prix de vente doit être supérieur à %d", record.property_id.best_price))

    @api.model_create_multi
    def create(self, vals_list):
        property_ids =[offer['property_id'] for offer in vals_list]
        properties = self.env["estate.property"].browse(property_ids)
        for property in properties:
            if property.state in ['Offer Accepted', 'Sold', 'Cancelled']:
                raise ValidationError(_("Aucune n'offre ne peut être réalisée sur cette propriété actuellement."))
        offers = super().create(vals_list)
        offers.property_id.state = 'Offer Received'
        return offers
