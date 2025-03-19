from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    vat_label = fields.Char(string='Tax ID Label', compute='_compute_vat_label')

    @api.depends_context('company')
    def _compute_vat_label(self):
        self.vat_label = self.env.company.country_id.vat_label or ("VAT")

    def _get_company_details_from_vat(self, vat):
        company_details = self.read_by_vat(vat)
        company_data = company_details[0] if company_details else {}
        if company_data:
            partner_gid = company_data.get('partner_gid')
            if partner_gid:
                company_data = self.enrich_company(company_domain=None, partner_gid=partner_gid, vat=company_data.get('vat'))
            return {
                'name': company_data.get('name'),
                'company_type': 'company',
                'partner_id': partner_gid,
                'street': company_data.get('street'),
                'street2': company_data.get('street2'),
                'city': company_data.get('city'),
                'state_id': company_data.get('state_id', {}).get('id', False),
                'country_id': company_data.get('country_id', {}).get('id', False),
                'zip': company_data.get('zip'),
                'vat': company_data.get('vat'),
            }
        return {}
