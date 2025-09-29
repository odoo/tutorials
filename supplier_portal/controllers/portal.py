from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers import portal
import base64


class BillsPortal(portal.CustomerPortal):
    @http.route(['/upload/bill',
                 ], type='http', auth='user', website=True, methods=['GET', 'POST'])
    def portal_upload_bill(self):
        values = {}
        partner_id = request.env['res.users'].sudo().browse(
            request.session.uid).partner_id
        organization = partner_id.parent_id if partner_id else False
        values.update({'organization': organization})
        if request.httprequest.method == 'POST':
            AccountMove = request.env['account.move']
            IrAttachment = request.env['ir.attachment']
            pdf_file = request.httprequest.files.get('pdf')
            xml_file = request.httprequest.files.get('xml')
            if not ((pdf_file and pdf_file.filename) or (xml_file and xml_file.filename)):
                values.update(
                    {'message_error': 'You must atleast upload pdf or xml file of your bill'})
                return request.render('supplier_portal.portal_my_bills_form', values)
            bill_id = AccountMove.sudo().create(
                {'partner_id': partner_id.id, 'move_type': 'in_invoice'})
            for file in request.httprequest.files.values():
                if not file.filename:
                    continue
                IrAttachment.sudo().create({
                    'name': file.filename,
                    'datas': base64.encodebytes(file.read()),
                    'res_model': 'account.move',
                    'res_id': bill_id.id,
                    'type': 'binary',
                })
            values.update(
                {'message_success': 'You have Successfully Uploaded Your bill'})
            return request.render('supplier_portal.portal_my_bills_form', values)
        return request.render('supplier_portal.portal_my_bills_form', values)
