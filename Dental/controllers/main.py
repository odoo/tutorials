from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class DentalPortal(CustomerPortal):
    @http.route('/my/dental', type='http', auth='user', website=True)
    def portal_my_dental(self, **kw):
        patients = request.env['dental.patient'].search([('guarantor_name', '=', request.env.user.id)])
        return request.render('Dental.portal_my_dental', {
            'users': patients
        })

    @http.route('/my/dental/<int:patient_id>', type='http', auth='user', website=True)
    def portal_my_dental_user(self, patient_id, **kw):
        patient = request.env['dental.patient'].browse(patient_id)
        return request.render('Dental.portal_my_dental_user', {
            'patient': patient
        })

    @http.route('/my/dental/<int:patient_id>/personal', type='http', auth='user', website=True)
    def portal_my_dental_personal(self, patient_id, **kw):
        patient = request.env['dental.patient'].browse(patient_id)
        return request.render('Dental.portal_my_dental_personal', {
            'patient': patient
        })

    @http.route('/my/dental/medical_history/<int:history_id>', type='http', auth='user', website=True)
    def portal_dental_medical_history_detail(self, history_id, **kw):
        medical_history = request.env['dental.medical.history'].browse(history_id)
        if not medical_history.exists():
            return request.not_found()
        return request.render('Dental.portal_my_dental_medical_history_detail', {
            'record': medical_history
        })

    @http.route('/my/dental/<int:patient_id>/medical_history', type='http', auth='user', website=True)
    def portal_my_dental_medical_history_list(self, patient_id, **kw):
        history = request.env['dental.medical.history'].search([('patient_id', '=', patient_id)])
        return request.render('Dental.portal_my_dental_medical_history_list', {
            'history': history
        })

    @http.route('/my/dental/<int:patient_id>/medical_aid', type='http', auth='user', website=True)
    def portal_my_dental_medical_aid(self, patient_id, **kw):
        medical_aid = request.env['dental.patient'].browse(patient_id).medical_aids
        return request.render('Dental.portal_my_dental_medical_aid', {
            'medical_aid': medical_aid
        })

    @http.route('/my/dental/<int:patient_id>/dental_history', type='http', auth='user', website=True)
    def portal_my_dental_dental_history(self, patient_id, **kw):
        dental_patient_history = request.env['dental.medical.history'].search([('patient_id', '=', patient_id)])
        return request.render('Dental.portal_my_dental_dental_history', {
            'dental_patient_history': dental_patient_history
        })
