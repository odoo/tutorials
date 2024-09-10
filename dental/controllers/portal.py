import math
from odoo.http import Controller, route, request


class PortalDental(Controller):

    @route(
        ["/my/dental", "/my/dental/page/<int:page>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_dental(self, page=1, per_page=6, **kw):
        page = int(page)
        per_page = int(per_page)
        offset = (page - 1) * per_page
        limit = per_page
        current_user = request.env.user
        domain = [("guaranator", "=", current_user.id)]
        patients = (
            request.env["dental.patients"]
            .sudo()
            .search(domain, limit=limit, offset=offset)
        )
        total_patinets = patients.search_count(domain)
        total_pages = math.ceil(total_patinets / per_page)
        pager = {
            "url": "/my/dental/page/" + str(page),
            "total": total_patinets,
            "current_page": page,
            "total_page": total_pages,
            "step": per_page,
        }
        values = {"patients": patients, "pager": pager}
        return request.render("dental.dental_patient_template", values)

    @route(
        "/my/dental/<string:name>/<int:patient_id>",
        type="http",
        auth="public",
        website=True,
    )
    def portal_dental_patient(self, patient_id, **kw):
        patients = request.env["dental.patients"].sudo().browse(patient_id)
        values = {"patient": patients}
        return request.render("dental.dental_individual_patient_template", values)

    @route(
        "/my/dental/<string:name>/<int:patient_id>/<string:data>",
        type="http",
        auth="public",
        website=True,
    )
    def portal_dental_patient_data(
        self, patient_id, data, sortby=None, filterby=None, **kw
    ):
        patient = request.env["dental.patients"].sudo().browse(patient_id)
        if not patient.exists():
            return request.render("website.page_404", {})
        elif data == "dentalhistory":
            domain = [("patient", "=", patient.id)]
            if filterby is None:
                filterby = "all"
                # pass the filter as tuple in search domain
            patient_history = (
                request.env["dental.history"].sudo().search(domain, order=sortby)
            )
            values = {
                "patient": patient,
                "patient_history": patient_history,
                "sort_by": sortby,
                "filter_by": filterby,
            }
            return request.render("dental.dental_patient_history_template", values)
        elif data == "personal":
            values = {"patient": self.patient_data(patient_id)}
            return request.render("dental.dental_patient_personal_template", values)
        elif data == "medical_history":
            values = {"history": self.patient_medical_history(patient_id)}
            return request.render(
                "dental.dental_patient_medical_history_template", values
            )
        elif data == "medical_aid":
            values = {
                "medical_aid": self.patient_medical_aid(patient_id),
                "patient": patient,
            }
            return request.render("dental.dental_patient_medical_aid_template", values)

        return request.render("website.page_404", {})

    def patient_data(self, patient_id):
        return request.env["dental.patients"].sudo().browse(patient_id)

    def patient_medical_history(self, patient_id):
        history = (
            request.env["dental.history"]
            .sudo()
            .search([("patient", "=", patient_id)], order="date")
        )
        return history[len(history) - 1]

    def patient_medical_aid(self, patient_id):
        patient = request.env["dental.patients"].sudo().browse(patient_id)
        return request.env["dental.medical.aid"].sudo().browse(patient.medical_aid.id)

    @route(
        "/my/dental/<string:name>/<int:patient_id>/medical_history/<int:history_id>",
        type="http",
        auth="public",
        website=True,
    )
    def medical_history_individual(self, name, patient_id, history_id, **kw):
        history = request.env["dental.history"].sudo().browse(history_id)
        patient = request.env["dental.patients"].sudo().browse(patient_id)
        values = {"history": history, "patient": patient}
        return request.render(
            "dental.dental_patient_medical_history_clicked_template", values
        )
