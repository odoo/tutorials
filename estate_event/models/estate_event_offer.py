from odoo import api, fields, models


class EstatePropertyEventOffer(models.Model):
    _inherit = "estate.property.offer"

    a_id = fields.Many2one('estate.property.visit')

    allowed_partner_ids = fields.Many2many(
        "res.partner",
        compute="_compute_allowed_partners"
    )

    partner_id = fields.Many2one(
        "res.partner",
        domain="[('id', 'in', allowed_partner_ids)]",
        required=True
    )

    @api.depends(
        'property_id.event_id.registration_ids.state',
        'property_id.event_id.registration_ids.partner_id',
        "property_id.visit_ids.partner_id",
        "a_id.partner_id",
        'a_id.date',
    )
    def _compute_allowed_partners(self):
        for rec in self:
            partners = self.env['res.partner']
            now = fields.Datetime.now()
            if rec.property_id.event_id:
                registrations = self.env['event.registration'].search([
                ('event_id', '=', rec.property_id.event_id.id)])
                partners |= registrations.mapped('partner_id')

            if rec.property_id:
                for visit in rec.property_id.visit_ids:
                    if visit.date <= now:
                        partners |= visit.partner_id

            if rec.a_id and rec.a_id.partner_id and rec.a_id.date:
                if rec.a_id.date <= now:
                    partners |= rec.a_id.partner_id
            rec.allowed_partner_ids = partners
