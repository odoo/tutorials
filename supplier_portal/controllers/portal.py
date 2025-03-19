# -*- coding: utf-8 -*-
from datetime import date
import datetime
from odoo import http
from odoo.http import request, route
from odoo.exceptions import AccessError
import base64

class SupplierPortal(http.Controller):

    @route(['/my/supplier_portal'], type='http', auth="user", website=True)
    def supplier_portal(self, **kw):
        return request.render("supplier_portal.supplier_portal_login_success", {})

    @route(['/my/supplier_portal/upload_invoice'], type='http', auth="user", methods=['POST'], website=True)
    def upload_invoice(self, **post):
        supplier = request.env.user.partner_id
        organisation_id = int(post.get('organisation_id'))
        
        # Get uploaded files
        pdf_file = post.get('pdf_file')
        xml_file = post.get('xml_file')

        # Read and encode files
        pdf_content = pdf_file.read()
        xml_content = xml_file.read()

        today = date.today()

        # Create vendor bill (Draft state)
        bill_vals = {
            'partner_id': supplier.id,
            'company_id': organisation_id,
            'invoice_date': today,
            'invoice_date_due': today+datetime.timedelta(days=7),
            'state': 'draft',
            'move_type': 'in_invoice',  # Vendor Bill
            'invoice_line_ids': [],
        }
        bill = request.env['account.move'].sudo().create(bill_vals)

        # Attach files
        request.env['ir.attachment'].sudo().create({
            'name': pdf_file.filename,
            'type': 'binary',
            'datas': base64.b64encode(pdf_content),
            'res_model': 'account.move',
            'res_id': bill.id,
        })

        request.env['ir.attachment'].sudo().create({
            'name': xml_file.filename,
            'type': 'binary',
            'datas': base64.b64encode(xml_content),
            'res_model': 'account.move',
            'res_id': bill.id,
        })

        return request.render('supplier_portal.supplier_portal_upload_success',{})
