# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import datetime
import io
import json

import requests
from requests.exceptions import RequestException
from werkzeug.urls import url_join

from odoo import http
from odoo.addons.sign.controllers.main import Sign
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.tools.pdf import PdfFileReader, PdfReadError

CASHFREE_API_BASE_URL = 'https://sandbox.cashfree.com/verification/esignature'


class SignController(Sign):

    def _validate_auth_method(self, request_item_sudo, sms_token=None):
        if request_item_sudo.role_id.auth_method == 'aadhar_esign':
            return {'success': True}
        super()._validate_auth_method(request_item_sudo, sms_token)

    @http.route('/sign/upload_document', type='http', auth='public', methods=['POST'], csrf=False, cors='*')
    def upload_document(self):
        file = request.httprequest.files.getlist('document')
        Config = request.env['ir.config_parameter'].sudo()

        client_id = Config.get_param('cashfree_client_id')
        client_secret = Config.get_param('cashfree_client_secret')

        if not file:
            return json.dumps({'error': 'No document uploaded'})
        file_data = file[0].read()
        url = url_join(CASHFREE_API_BASE_URL + '/', 'document')
        headers = {
            'x-client-id': str(client_id),
            'x-client-secret': str(client_secret),
        }
        files = {
            'document': (file[0].filename, file_data)
        }
        response = requests.post(url, headers=headers, files=files)
        return json.dumps(response.json())

    @http.route('/sign/verify_esignature', type='http', auth='public', csrf=False, cors='*')
    def verify_esignature(self):
        verification_id = request.params.get('verification_id')
        Config = request.env['ir.config_parameter'].sudo()

        client_id = Config.get_param('cashfree_client_id')
        client_secret = Config.get_param('cashfree_client_secret')

        headers = {
            "x-client-id": str(client_id),
            "x-client-secret": str(client_secret)
        }
        params = {
            "verification_id": verification_id
        }
        try:
            response = requests.get(CASHFREE_API_BASE_URL, headers=headers, params=params)
            return json.dumps(response.json())
        except RequestException as e:
            return {"status": "ERROR", "message": str(e)}

    @http.route('/e_sign/create_request', type='http', auth='public', methods=['POST'], csrf=False)
    def send_signer_details(self):
        signers_list = []
        Config = request.env['ir.config_parameter'].sudo()
        client_id = Config.get_param('cashfree_client_id')
        client_secret = Config.get_param('cashfree_client_secret')
        user_data = request.httprequest.get_data()
        parsed_data = json.loads(user_data.decode("utf-8"))
        document_id = parsed_data.get("document_id")
        verification_id = parsed_data.get("verification_id")
        expiry_days = parsed_data.get("expiry_days")
        signers = parsed_data.get("signers")
        redirect_url = parsed_data.get("redirect_url")
        if expiry_days > 15:
            expiry_days = 15
        for index, signer in enumerate(signers, start=1):
            signer_data = {
                "name": str(signer['name']),
                "email": str(signer['email']),
                "sequence": index,
                "sign_positions": [
                    {
                        "page": int(pos['page']),
                        "top_left_x_coordinate": int(pos['top_left_x_coordinate']),
                        "bottom_right_x_coordinate": int(pos['bottom_right_x_coordinate']),
                        "top_left_y_coordinate": int(pos['top_left_y_coordinate']),
                        "bottom_right_y_coordinate": int(pos['bottom_right_y_coordinate'])
                    }
                    for pos in signer['sign_positions']
                ],
                "phone": signer.get('phone'),
                "aadhaar_last_four_digit": str(signer.get('aadhaar_last_four_digit')),
            }
            signers_list.append(signer_data)
            payload = {
                "verification_id": str(verification_id),
                "document_id": document_id,
                "notification_modes": ["email"],
                "auth_type": "AADHAAR",
                "expiry_in_days": str(expiry_days),
                "signers": signers_list,
                "redirect_url": redirect_url
            }
            headers = {
                "x-client-id": str(client_id),
                "x-client-secret": str(client_secret),
                "Content-Type": "application/json"
            }
            try:
                response = requests.post(
                    CASHFREE_API_BASE_URL,
                    json=payload,
                    headers=headers,
                    timeout=10
                )
                res_data = json.dumps(response.json())
                return res_data
            except requests.exceptions.RequestException as e:
                return {"status": "ERROR", "message": str(e)}

    @http.route(['/sign/data/<int:request_id>/<token>'], auth='public')
    def get_data(self, request_id, token):
        try:
            sign_request = http.request.env['sign.request'].sudo().browse(request_id).exists()
            if not sign_request or sign_request.access_token != token:
                return http.request.not_found()
            validity_date = sign_request.validity
            today = datetime.date.today()
            expiry_in_days = (validity_date - today).days if validity_date else 0
            signers_data = []
            old_pdf = PdfFileReader(io.BytesIO(base64.b64decode(sign_request.template_id.attachment_id.datas)), strict=False, overwriteWarnings=False)
            itemsByPage = sign_request.template_id._get_sign_items_by_page()
            for signer in sign_request.request_item_ids:
                signer_info = {
                    'name': signer.partner_id.name,
                    'email': signer.partner_id.email,
                    'phone': signer.partner_id.phone,
                    'sign_positions': []
                }
                for p in range(0, old_pdf.getNumPages()):
                    page = old_pdf.getPage(p)
                    width = float(abs(page.mediaBox.getWidth()))
                    height = float(abs(page.mediaBox.getHeight()))
                    items = itemsByPage.get(p + 1, [])
                    for item in items:
                        if item.responsible_id.name == signer.role_id.name:
                            signer_info['sign_positions'].append({
                                'page': item.page,
                                'top_left_X': int(width * item.posX),
                                'top_left_Y': int(height * (1 - item.posY)),
                                'bottom_right_X': int(width * item.posX) + (width * item.width),
                                'bottom_right_Y': int(height * (1 - item.height - item.posY)),
                            })
                signers_data.append(signer_info)
            result = {
                'filename': f"{sign_request.reference}",
                'mimetype': 'application/pdf',
                'expiry_in_days': expiry_in_days,
                'signers': signers_data,
            }
            res_data = json.dumps(result)
            return res_data
        except PdfReadError as e:
            return http.Response(json.dumps({"error": "PDF error: " + str(e)}), content_type='application/json', status=500)
        except (AttributeError, TypeError, KeyError) as e:
            return http.Response(json.dumps({"error": "Data error: " + str(e)}), content_type='application/json', status=500)

    @http.route(['/sign/file/<int:request_id>/<token>'], auth='public')
    def get_file(self, request_id, token):
        try:
            sign_request = http.request.env['sign.request'].sudo().browse(request_id).exists()
            if not sign_request or sign_request.access_token != token:
                return http.request.not_found()
            document = None
            if sign_request.completed_document:
                document = sign_request.completed_document
            elif sign_request.template_id.attachment_id:
                document = sign_request.template_id.attachment_id.datas
            if not document:
                return {'error': 'Document not found'}
            document = base64.b64decode(document)
            return http.Response(document, headers=[
                ('Content-Type', 'application/pdf'),
            ])
        except (AccessError, MissingError) as e:
            return http.Response(json.dumps({"error": str(e)}), content_type='application/json', status=500)
