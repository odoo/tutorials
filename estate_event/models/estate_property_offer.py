from odoo import models, fields, api

from odoo.fields import Datetime


class EstatePropertyOffer(models.Model):
    _inherit = "estate.property.offer"

    available_partner_ids = fields.Many2many("res.partner", compute="_compute_available_partner_ids")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True, domain="[('id', 'in', available_partner_ids)]")

    @api.depends('property_id')
    def _compute_available_partner_ids(self):
        for record in self:
            partners = self.env['res.partner']
            if record.property_id:
                event = self.env['event.event'].search([('property_id', '=', record.property_id._origin.id)], limit=1)
                registrations = self.env['event.registration'].search([
                    ('event_id', '=', event.id),
                    ('state', '=', 'done')
                ])
                emails = registrations.mapped('email')
                event_partners = self.env['res.partner'].search([('email', 'in', emails)])
                visits = self.env['estate.property.visit'].search([
                    ('propert_id', '=', record.property_id._origin.id),
                    ('end_date', '<=', Datetime.now())
                    ])
                visit_partners = visits.mapped('partner_id')
                partners = visit_partners | event_partners
            record.available_partner_ids = partners

    # @api.model_create_multi
    # def create(self, vals_list):
    #     records = super().create(vals_list)
    #     for record in records:
    #         event = self.env['event.event'].search([('property_id', '=', record.property_id.id)], limit=1)

    #         registration = self.env['event.registration'].search([
    #             ('event_id', '=', event.id),
    #             ('partner_id', '=', record.partner_id.id),
    #             ('state', '=', 'done')
    #         ], limit=1)
    #         if not registration:
    #             raise UserError("This partner has not attended the event.")
    #     return records
