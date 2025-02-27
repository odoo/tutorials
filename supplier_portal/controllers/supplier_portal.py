import base64
from odoo import http
from odoo.http import request, route
from odoo.tools.mimetypes import guess_mimetype

class SupplierPortal(http.Controller):

    @route('/supplier_portal', auth="user", website=True)
    def supplier_portal(self, **kwargs):
        message = kwargs.get('message', '')
        return request.render("supplier_portal.supplier_portal_template", {'message': message})
    
    @route('/supplier_portal/create_draft_bill', type="http", methods=['GET'], website=True, auth="user")
    def redirect_supplier_portal(self, **kwargs):
        return request.redirect('/supplier_portal')
    
    @route('/supplier_portal/create_draft_bill', type="http", methods=['POST'], website=True, auth="user", csrf=False)
    def create_draft_bill(self, **kwargs):
        company_id = kwargs.get('company_id')
        message = ""
        attachments = []
        valid_file_uploaded = False 

        pdf_file = request.httprequest.files.get('pdf_file')
        xml_file = request.httprequest.files.get('xml_file')

        if not company_id:
            return request.render("supplier_portal.supplier_portal_template", {'message': "Please select a company"})

        for file, mimetype in [(pdf_file, 'application/pdf'), (xml_file, 'application/xml')]:
            if file:
                file_content = file.read() 
                if mimetype == guess_mimetype(file_content):
                    file_data = base64.b64encode(file_content).decode('utf-8') 
                    attachment = request.env["ir.attachment"].sudo().create({
                        'name': file.filename,
                        'datas': file_data,
                        'mimetype': mimetype,
                        'res_model': 'account.move'
                    })
                    attachments.append(attachment.id)
                    valid_file_uploaded = True
                else:
                    message += f"Invalid file type for {file.filename}! " 

        if not valid_file_uploaded:
            message = "No valid file uploaded!"
            return request.render("supplier_portal.supplier_portal_template", {'message': message})
            
        draft_bill = request.env['account.move'].sudo().create({
            'move_type': 'in_invoice',
            'partner_id': request.env.user.partner_id.id,
            'company_id': int(company_id),
            'state': 'draft'
        })

        if attachments:
            request.env['ir.attachment'].browse(attachments).sudo().write({'res_id': draft_bill.id})

        if not message: 
            message = "Draft bill created successfully!"

        return request.render("supplier_portal.supplier_portal_template", {'message': message})
