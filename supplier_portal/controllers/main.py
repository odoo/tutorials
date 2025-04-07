import base64
from odoo import http
from odoo.http import request
from odoo.exceptions import UserError


class SupplierPortal(http.Controller):
    @http.route('/supplier_portal', auth='user', type='http', website=True)
    def show_supplier_portal(self, *args, **kwargs):
        return request.render('supplier_portal.supplier_portal_template', {})

    @http.route('/supplier_portal_thank_you', auth='user', type='http', website=True)
    def show_supplier_portal_thank_you(self):
        return request.render('supplier_portal.supplier_portal_thank_you_template')

    @http.route('/submit_supplier_portal_form', auth='user', type='http', website=True)
    def submit_supplier_portal_form(self, *args, **kwargs):
        partner_id = request.env.user.partner_id.id

        # Creating invoice
        in_invoice = request.env['account.move'].sudo().create({
            'move_type': 'in_invoice',
            'partner_id': partner_id,
            'company_id': int(kwargs.get('company_id')),
        })

        if not in_invoice:
            raise UserError("Something went wrong!!!")

        # Creating attachments
        request.env['ir.attachment'].sudo().create({
            'datas': base64.b64encode(kwargs.get('pdf_file').read()),
            'type': 'binary',
            'name': 'invoice.pdf',
            'mimetype': 'application/pdf',
            'res_model': 'account.move',
            'res_id': in_invoice.id,
        })
        request.env['ir.attachment'].sudo().create({
            'datas': base64.b64encode(kwargs.get('xml_file').read()),
            'type': 'binary',
            'name': "invoice.xml",
            'mimetype': 'text/xml',
            'res_model': 'account.move',
            'res_id': in_invoice.id,
        })

        return request.redirect("/supplier_portal_thank_you")
