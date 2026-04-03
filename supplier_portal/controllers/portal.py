from odoo import http
from odoo.http import request
import base64


class SupplierPortal(http.Controller):
    @http.route('/my/invoice/upload', type='http', auth='user', website=True)
    def invoice_form(self, **kw):

        partner = request.env.user.partner_id
        companies = partner.allowed_company_ids

        return request.render(
            'supplier_portal.portal_invoice_upload', {'companies': companies}
        )

    @http.route(
        '/my/invoice/upload/submit',
        type='http',
        auth='user',
        methods=['POST'],
        website=True,
        csrf=True,
    )
    def invoice_submit(self, **post):

        partner = request.env.user.partner_id
        company_id = int(post.get('company_id'))
        file1 = request.httprequest.files.get('file1')
        file2 = request.httprequest.files.get('file2')

        if not file1 or not file1.filename.lower().endswith('.xml'):
            return request.render(
                'supplier_portal.portal_invoice_upload',
                {
                    'error': 'Please upload a valid XML file',
                    'companies': request.env.user.partner_id.allowed_company_ids,
                },
            )

        if not file2 or not file2.filename.lower().endswith('.pdf'):
            return request.render(
                'supplier_portal.portal_invoice_upload',
                {
                    'error': 'Please upload a valid PDF file',
                    'companies': request.env.user.partner_id.allowed_company_ids,
                },
            )

        if company_id not in partner.allowed_company_ids.ids:
            return request.redirect('/my')

        invoice = (
            request.env['account.move']
            .sudo()
            .create(
                {
                    'move_type': 'in_invoice',
                    'partner_id': partner.id,
                    'company_id': company_id,
                }
            )
        )

        for file in [file1, file2]:
            if file:
                request.env['ir.attachment'].sudo().create(
                    {
                        'name': file.filename,
                        'type': 'binary',
                        'datas': base64.b64encode(file.read()),
                        'res_model': 'account.move',
                        'res_id': invoice.id,
                    }
                )

        return request.redirect('/my')
