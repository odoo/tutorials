from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class DentalPortal(CustomerPortal):
    @http.route('/my/dental', type='http', auth='user', website=True)
    def portal_my_dental(self, **kw):
        current = request.env.user.id
        users = request.env['dental.patient'].search([('guarantor_id', '=', current)])
        return request.render('dental.portal_my_dental', {
            'users': users
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
        medical_historys = request.env['medical.history'].search([('patient_id', '=', patient_id)])
        return request.render('dental.portal_my_dental_medical_history', {
            'medical_historys': medical_historys
        })

    @http.route('/my/dental/<int:patient_id>/medical_aid', type='http', auth='user', website=True)
    def portal_my_dental_medical_aid(self, patient_id, **kw):
        medical_aid = request.env['dental.patient'].search([]).insurance_id
        return request.render('dental.portal_my_dental_medical_aid', {
            'medical_aid': medical_aid
        })

    @http.route('/my/dental/<int:patient_id>/dental_history', type='http', auth='user', website=True)
    def portal_my_dental_dental_history(self, patient_id, **kw):

        return request.render('dental.portal_my_dental_dental_history', {
        })
