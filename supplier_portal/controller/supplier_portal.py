# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64

from odoo import http
from odoo.http import request

class SupplierPortal(http.Controller):

    @http.route('/supplier_portal', type='http', auth='user', website=True)
    def supplier_portal(self):
        return request.render('supplier_portal.supplier_portal_template')

    @http.route('/supplier_portal/submit', type='http', auth='user', website=True, methods=['POST'])
    def supplier_portal_submit(self, **kwargs):
        company_id = int(kwargs.get('company'))
        pdf_file = kwargs.get('pdf_file')
        xml_file = kwargs.get('xml_file')
        user = request.env.user

        if user.company_id.id != company_id:
            user.company_id = company_id

        partner = user.partner_id

        bill = request.env['account.move'].sudo().with_company(company_id).create({
            'move_type': 'in_invoice',
            'partner_id': partner.id,
            'company_id': company_id,
        })

        files = [
            ("invoice.pdf", pdf_file, 'application/pdf'),
            ("invoice.xml", xml_file, 'application/xml'),
        ]

        attachments = []
        for file_name, file_obj, mime_type in files:
            file_content = file_obj.read()
            if file_content:
                attachments.append({
                    'res_id': bill.id,
                    'res_model': 'account.move',
                    'name': file_name,
                    'datas': base64.b64encode(file_content),
                    'type': 'binary',
                    'mimetype': mime_type,
                })

        if attachments:
            request.env['ir.attachment'].sudo().create(attachments)

        return request.render('supplier_portal.generic_message', {
            'message': "Document uploaded successfully."
        })
