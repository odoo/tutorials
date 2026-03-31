from odoo import api, models, fields
from odoo.exceptions import UserError


class EstateOfferWizard(models.TransientModel):
    _name = "estate.offer.wizard"
    _description = "create offer wizard"

    allowed_partner_ids = fields.Many2many(
        "res.partner",
        compute="_compute_allowed_partner_ids",
        store=False,
    )

    buyer_id = fields.Many2one('res.partner', required=True)
    price = fields.Float(required=True)

    @api.depends_context("active_ids")
    def _compute_allowed_partner_ids(self):
        active_ids = self.env.context.get("active_ids", [])
        properties = self.env["estate.property"].browse(active_ids)

        allowed_partners = None
        for property in properties:
            partners_properties = self.env["res.partner"]

            if property.event_id:
                registrations = property.event_id.registration_ids.filtered(
                    lambda record: record.state == "done"
                )
                partners_properties |= registrations.mapped("partner_id")

            visits = property.visit_ids.filtered(lambda record: record.state == "done")
            partners_properties |= visits.mapped("partner_id")

            if allowed_partners is None:
                allowed_partners = partners_properties
            else:
                allowed_partners &= partners_properties
        allowed_partners = allowed_partners or self.env["res.partner"]

        for wizard in self:
            wizard.allowed_partner_ids = allowed_partners

    def action_create_offer(self):
        active_ids = self.env.context.get("active_ids")
        properties = self.env["estate.property"].browse(active_ids)

        for property in properties:
            if property.state not in ['new', 'offer_received']:
                raise UserError("offers can be created if the stage is in, 'new' or 'offer received'")

            self.env['estate.property.offer'].create({
                'property_id': property.id,
                'partner_id': self.buyer_id.id,
                'price': self.price,
            })
