import math
from odoo import http
from odoo.http import request


class DentalController(http.Controller):

    @http.route(
        ["/home/dental", "/home/dental/page/<int:page>"],
        type="http",
        auth="public",
        website=True,
    )
    def show_all_the_data(self, page=1, **kwargs):
        patients_per_page = 2
        current_user = request.env.user
        total_patients = (
            request.env["dental.patient"]
            .sudo()
            .search_count([("gurantor", "=", current_user.id)])
        )

        pager = request.website.pager(
            url="/home/dental/",
            total=total_patients,
            page=page,
            step=patients_per_page,
        )

        patients = (
            request.env["dental.patient"]
            .sudo()
            .search(
                [("gurantor", "=", current_user.id)],
                offset=pager["offset"],
                limit=patients_per_page,
            )
        )
        return request.render(
            "dental.dental_card_controller",
            {"patients": patients, "pager": pager},
        )

    @http.route(
        ["/home/dental/<int:record_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def show_patient_details(self, record_id, **kwargs):
        custom_data = request.env["dental.patient"].sudo().browse(record_id)

        return request.render(
            "dental.patient_details_controller",
            {
                "patients": custom_data,
            },
        )

    @http.route(
        ["/home/dental/appointment/<int:record_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def show_patient_medical_appointment(self, record_id, **kwargs):
        custom_data = request.env["dental.patient"].sudo().browse(record_id)
        custom_history = custom_data.history_ids

        return request.render(
            "dental.patient_details_controller_appointment",
            {
                "patients": custom_history,
            },
        )

    @http.route(
        ["/home/dental/personal/<int:record_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def show_patient_medical_personal(self, record_id, **kwargs):
        custom_data = request.env["dental.patient"].sudo().browse(record_id)
        return request.render(
            "dental.patient_my_dental_personal",
            {
                "patients": custom_data,
            },
        )

    @http.route(
        ["/home/dental/medicalaid/<int:record_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def show_patient_medical_aids(self, record_id, **kwargs):
        custom_data = request.env["dental.patient"].sudo().browse(record_id)
        medical_aids = custom_data.medicalaid_id
        return request.render(
            "dental.patient_my_dental_medical_aids",
            {
                "patients": medical_aids,
            },
        )

    @http.route(
        ["/home/dental/history/form/<int:record_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def show_patient_medical_history_form(self, record_id, **kwargs):
        custom_data = request.env["patient.history"].sudo().browse(record_id)
        print(custom_data.name)
        return request.render(
            "dental.patient_my_dental_medical_history_form",
            {
                "patient": custom_data,
            },
        )

    @http.route(
        ["/home/dental/hisory/<int:record_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def show_patient_medical_history_table(self, record_id, **kwargs):
        custom_data = request.env["dental.patient"].sudo().browse(record_id)
        custom_history = custom_data.history_ids

        return request.render(
            "dental.patient_details_controller_history_table",
            {
                "patients": custom_history,
            },
        )
