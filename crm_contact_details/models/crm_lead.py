# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Lead(models.Model):
    _inherit = 'crm.lead'

    address_detail_ids = fields.Many2many(
        'res.partner',
        string="Address Details",
        domain="[('parent_id', '=', partner_id), ('type', '=', 'delivery')]",
    )
    contact_detail_ids = fields.Many2many(
        'res.partner', 'crm_lead_contact_detail_default_rel', 'lead_id', 'partner_id',
        string="Contact Details",
        compute="_compute_contact_details",
        inverse="_inverse_contact_details",
        domain="[('parent_id', '=', selected_address_id), ('type', '=', 'contact')]",
        store=True,
    )
    selected_address_id = fields.Many2one(
        'res.partner',
        string="Selected Address",
        compute="_compute_single_address_selection",
        store=True,
    )

    @api.onchange('partner_id')
    def _onchange_address_details(self):
        self.address_detail_ids = None
        self.contact_detail_ids = None
        self.selected_address_id = False
        if self.partner_id:
            for address in self.partner_id.child_ids.filtered(lambda p: p.type == 'delivery'):
                address.is_selected = False
                for contact in address.child_ids.filtered(lambda c: c.type == 'contact'):
                    contact.show_in_contact_detail = True

    @api.depends('address_detail_ids')
    def _compute_contact_details(self):
        for lead in self:
            if lead.address_detail_ids:
                lead.contact_detail_ids = lead.address_detail_ids.child_ids.filtered(lambda c: c.type == 'contact' and c.show_in_contact_detail)
            else:
                lead.contact_detail_ids = None

    def _inverse_contact_details(self):
        for lead in self:
            all_contacts = lead.address_detail_ids.child_ids.filtered(lambda c: c.type == 'contact')
            latest_removed_contacts = all_contacts.filtered(lambda c: c.show_in_contact_detail and c not in lead.contact_detail_ids)
            # Check validation for remove only selected address contact person.
            invalid_contacts = latest_removed_contacts.filtered(lambda c: c.parent_id.id != lead.selected_address_id.id)
            if invalid_contacts:
                raise ValidationError(
                    f"You can only remove contact persons linked to the selected address: "
                    f"{lead.selected_address_id.display_name}"
                )
            # Remove contacts
            for contact in latest_removed_contacts:
                if contact.show_in_contact_detail:
                    contact.show_in_contact_detail = False
            # Add contacts
            for contact in lead.contact_detail_ids:
                if not contact.show_in_contact_detail:
                    contact.show_in_contact_detail = True

    @api.depends('address_detail_ids.is_selected')
    def _compute_single_address_selection(self):
        """Ensure only one address is selected at a time."""
        for lead in self:
            if lead.selected_address_id:
                lead.selected_address_id.is_selected = False
            selected_addresses = lead.address_detail_ids.filtered(lambda p: p.is_selected)
            if selected_addresses:
                latest_address = selected_addresses[-1]
                for address in lead.address_detail_ids:
                    if address != latest_address:
                        address.is_selected = False
                    else:
                        address.is_selected = True
                lead.selected_address_id = latest_address
            else:
                lead.selected_address_id = False
