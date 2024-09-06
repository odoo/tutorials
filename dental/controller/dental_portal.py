from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class DentalPortal(CustomerPortal):
    @http.route('/my/dental', type='http', auth='user', website=True)
    def portal_my_dental(self, **kw):
        patients = request.env['dental.patient'].search([('guarantor_id', '=', request.env.user.id)])
        return request.render('dental.portal_my_dental', {
            'patients': patients
        })

    @http.route('/my/dental/<int:patient_id>', type='http', auth='user', website=True)
    def portal_my_dental_user(self, patient_id, **kw):
        patient = request.env['dental.patient'].browse(patient_id)
        return request.render('dental.portal_my_dental_user', {
            'patient': patient
        })

    @http.route('/my/dental/<int:patient_id>/personal', type='http', auth='user', website=True)
    def portal_my_dental_personal(self, patient_id, **kw):
        patient = request.env['dental.patient'].browse(patient_id)
        return request.render('dental.portal_my_dental_personal', {
            'patient': patient
        })

    @http.route('/my/dental/<int:patient_id>/medical_history', type='http', auth='user', website=True)
    def portal_my_dental_medical_history(self, patient_id, **kw):
        history = request.env['dental.patient.history'].search([('patient_id', '=', patient_id)])
        return request.render('dental.portal_my_dental_medical_history', {
            'history': history
        })

    @http.route('/my/dental/<int:patient_id>/medical_aid', type='http', auth='user', website=True)
    def portal_my_dental_medical_aid(self, patient_id, **kw):
        patient = request.env['dental.patient'].browse([patient_id])
        return request.render('dental.portal_my_dental_medical_aid', {
            'patient': patient
        })

    @http.route('/my/dental/<int:patient_id>/dental_history', type='http', auth='user', website=True)
    def portal_my_dental_dental_history(self, patient_id, **kw):
        history = request.env['dental.patient.history'].search([('patient_id', '=', patient_id)])
        return request.render('dental.portal_my_dental_dental_history', {
            'history': history,
            'patient_id': patient_id
        })

    @http.route('/my/dental/<int:patient_id>/dental_history/<int:history_id>', type='http', auth='user', website=True)
    def portal_my_dental_dental_history_details(self, patient_id, history_id, **kw):
        history_record = request.env['dental.patient.history'].browse(history_id)
        return request.render('dental.portal_my_dental_dental_history_details', {
            'history_record': history_record
        })
