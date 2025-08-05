# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Lead(models.Model):
    _inherit = "crm.lead"

    stage_sequence_no = fields.Integer(string="Stage Sequence No", related="stage_id.sequence_no")
    selected_address_partner_id = fields.Many2one('res.partner', string="Selected Address Partner",
                                                  compute="_compute_contact_details")
    address_detail_ids = fields.Many2many('res.partner', string="Address Details", domain="[('parent_id', '=', partner_id), ('type', '=', 'delivery')]", copy=False)
    contact_detail_ids = fields.Many2many('res.partner', 'crm_lead_contact_detail_default_rel', 'lead_id', 'partner_id', string="Contact Details", domain="[('parent_id', '=', selected_address_partner_id), ('type', '=', 'contact')]", compute="_compute_contact_details")
    is_contact_detail_editable = fields.Boolean(string="Is Contact Detail Editable", compute="_compute_contact_details")

    @api.depends("address_detail_ids.is_selected_line")
    def _compute_contact_details(self):
        for lead in self:
            address_detail_ids = lead.address_detail_ids
            lead.selected_address_partner_id = lead.is_contact_detail_editable = False
            lead.contact_detail_ids = address_detail_ids.child_ids.filtered(lambda c: c.type == 'contact')
            selected_partners = address_detail_ids.filtered('is_selected_line')
            if selected_partners:
                lead.update({
                    'selected_address_partner_id': selected_partners[0],
                    'is_contact_detail_editable': bool(len(selected_partners) == 1),
                    'contact_detail_ids': selected_partners.child_ids.filtered(lambda c: c.type == 'contact')
                })

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self.address_detail_ids = self.contact_detail_ids = False
