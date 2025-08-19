import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { Input } from "@point_of_sale/app/generic_components/inputs/input/input";
import { Component, useState } from "@odoo/owl";
import { unaccent } from "@web/core/utils/strings";

export class EmployeeList extends Component {
    static components = { Dialog, Input };
    static template = "pos_orderline_employee.EmployeeList";
    static props = {
        employee: {
            optional: true,
            type: [{ value: null }, Object],
        },
        getPayload: { type: Function },
        close: { type: Function },
    };

    setup() {
        this.pos = usePos();
        this.ui = useState(useService("ui"));
        this.dialog = useService("dialog");
        this.state = useState({
            query: null
        });
    }
    
    async editEmployee(e = false) {
        const employee = await this.pos.editEmployee(e);
        if (employee) {
            this.clickEmployee(employee);
        }
    }

    confirm() {
        this.props.resolve({ confirmed: true, payload: this.state.selectedPartner });
        this.pos.closeTempScreen();
    }

    getEmployees() {
        const searchWord = unaccent((this.state.query || "").trim(), false);
        const employees = this.pos.models["hr.employee"].getAll();
        employees.forEach((e) => {
            if (!e.searchString) {
                e.searchString = `${e.name || ""} ${e.work_contact_id.phone || ""}  ${e.work_contact_id.mobile || ""} ${e.work_contact_id.email || ""}`.toLowerCase();
            }
        });
        const availableEmployees = searchWord
        ? employees.filter((p) => p.searchString.includes(searchWord))
        : employees.slice(0, 1000).sort((a, b) =>
            this.props.employee?.id === a.id ? -1 :
            this.props.employee?.id === b.id ? 1 :
            (a.name || "").localeCompare(b.name || "")
        );

        return availableEmployees;
    }

    clickEmployee(employee) {
        this.props.getPayload(employee);
        this.props.close();
    }
}
