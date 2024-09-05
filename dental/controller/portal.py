from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal

class DentalPortal(CustomerPortal):

    @http.route(['/my/dental'], type='http', auth='public', website=True)
    def portal_my_dental(self, **kwargs):

        patients = request.env['dental.patient'].sudo().search([])

        values = {
            'patients': patients,
            'page_name': 'dental'
        }
        for patient in patients:
            print("Patient:", patient.guarantor_id.id)
        return request.render("dental.portal_my_dental", values)

    @http.route(['/my/dental/<int:patient_id>'], type='http', auth='public', website=True)
    def portal_my_dental_patient(self, patient_id, **kwargs):

        patient = request.env['dental.patient'].sudo().search(['guaranter_id', '=' , patient_id])

        values = {
            'patient': patient,
            'page_name': 'dental'
        }

        print("Values:", values)

        return request.render("dental.portal_my_dental_patient", values)