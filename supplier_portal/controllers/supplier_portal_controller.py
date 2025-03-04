# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
from datetime import datetime
from odoo import http
from odoo.http import request


class SupplierPortal(http.Controller):
    @http.route(['/supplier/portal'], type='http', auth='user', website=True)
    def supplier_portal(self):
        company_id = request.env.user.company_ids
        return request.render('supplier_portal.supplier_portal_template', {'company_id': company_id})

    @http.route(['/supplier/portal/submit'], type='http', auth='user', website=True)
    def submit_invoice(self, **post):
        supplier = request.env.user.partner_id
        company_id = post.get('company_id')
        if not company_id:
            return request.redirect('/supplier/portal?error=1')
        bill = request.env['account.move'].sudo().create({
            'move_type': 'in_invoice',
            'partner_id': supplier.id,
            'company_id': int(company_id)  ,
            'invoice_date': datetime.today(),
            'state': 'draft'
        })
        for file_param in ['pdf_file', 'xml_file']:
            file = post.get(file_param)
            if file:
                request.env['ir.attachment'].sudo().create({
                    'name': file.filename,
                    'datas': base64.b64encode(file.read()),
                    'res_model': 'account.move',
                    'res_id': bill.id
                })
        return request.redirect('/supplier/portal?success=1')
