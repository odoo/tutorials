from odoo import models
from odoo.http import request


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _can_be_edited_by_current_customer(self, sale_order, address_type):
        current_user = request.env.user
        if (current_user.has_group('base.group_portal') or current_user.has_group('base.group_system')):
         return sale_order, address_type

    def _get_company_details_from_vat(self, vat):
        company_details = self.read_by_vat(vat)
        company_data = company_details[0] if company_details else {}
        if company_data:
            partner_gid = company_data.get('partner_gid')
            if partner_gid:
                company_data = self.enrich_company(company_domain=None, partner_gid=partner_gid, vat=company_data.get('vat'))
            return {
                'name': company_data.get('name'),
                'partner_id': partner_gid,
                'vat': company_data.get('vat'),
            }
        return {}
