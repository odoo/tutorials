import { Component, useState } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";
import { SelectionPopup } from "@point_of_sale/app/utils/input_popups/selection_popup";

export class SelectSalesperson extends Component {
    static template = "point_of_sale.SelectSalesperson";
    // static props = ["salesperson?"];

    setup() {
        this.pos = usePos();
        this.dialog = useService("dialog");

        // Get the current order and initialize salesperson state
        const currentOrder = this.pos.get_order();
        this.state = useState({
            salesperson: currentOrder ? currentOrder.getSalesperson() : null,
        });
    }

    async selectSalesperson() {
        const currentOrder = this.pos.get_order();
        if (!currentOrder) {
            return false;
        }
        const employees = this.pos.models["hr.employee"] ;

        const employeeList = employees.map((emp) => ({
            id: emp.id,
            label:emp.name,
            item: emp,
            isSelected: currentOrder.getSalesperson()?.id === emp.id || false,
        }));

        const selectedEmployee = await makeAwaitable(this.dialog, SelectionPopup,{
            title: _t("Select a Salesperson"),
            list: employeeList
        });
        console.log(selectedEmployee)
        if(selectedEmployee){
            currentOrder.setSalesperson(selectedEmployee);
            this.state.salesperson = selectedEmployee;
        }
    }
}
