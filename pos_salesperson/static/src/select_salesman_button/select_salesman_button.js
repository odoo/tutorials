import { Component, useState } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { SelectionPopup } from "@point_of_sale/app/utils/input_popups/selection_popup";
import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";

export class SelectSalesPersonButton extends Component {
    static template = "point_of_sale.SelectSalesPersonButton";

    setup() {
        this.salesperson = useState({ name: "Salesperson" });
        this.pos = usePos();
        this.orm = useService("orm");
        this.dialog = useService("dialog");
    }

    async selectSalesman() {
        const currentOrder = this.pos.get_order();
        const employees = await this.getEmployees();

        if (employees.lenght === 0) {
            await makeAwaitable(this.dialog, AlertPopup, {
                title: "No Salesperson Available",
                body: "There are no employees available to select.",
            });
        }

        const employees_list = employees.map(emp => ({
            id: emp.id,
            label: emp.name,
            isSelected: false,
            item:emp
        }));

        const payload = await makeAwaitable(this.dialog, SelectionPopup, {
            title: "Select a Salesperson",
            list: employees_list
        });

        if (payload) {
            this.salesperson.name = payload.name;
            currentOrder.set_salesperson(payload.id);
        }
        else {
            this.salesperson.name = "Salesperson";
        }
    }

    async getEmployees() {
        return this.pos.models['hr.employee'] || [];
    }
}
