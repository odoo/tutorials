import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { SelectionPopup } from "@point_of_sale/app/utils/input_popups/selection_popup";
import { _t } from "@web/core/l10n/translation";
import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";

export class SelectSalespersonButton extends Component {
    static template = "pos_salesperson_assignment.SelectSalespersonButton";
    static props = {};

    setup() {
        this.pos = usePos();
        this.dialog = useService("dialog");
    }

    _prepareEmployeeList(currentSalesPerson) {
        const allEmployees = this.pos.models['hr.employee'].filter(
            (employee) => employee.id !== currentSalesPerson
        );

        const employeeList = allEmployees.map((employee) => {
            return {
                id: employee.id,
                item: employee,
                label: employee.name,
                isSelected: false
            }
        })

        return employeeList;
    }

    async onClick() {
        const order = this.pos.get_order();
        if (!order || order.lines.length <= 0) {
            return;
        }
    
        const employeesList = this._prepareEmployeeList(order.getSalesPerson()?.id);
    
        if (!employeesList.length) {
            return;
        }
    
        let sales_person = await makeAwaitable(this.dialog, SelectionPopup, {
            title: _t("Select Sales Person"),
            list: employeesList
        });
    
        if (!sales_person) {
            return;
        }
        
        order.setSalesPerson(sales_person);
    }

    async onRemove() {
        const order = this.pos.get_order();
        if (!order || !order.sales_person_id) {
            return;
        }

        order.setSalesPerson(false);
    }
    
    get salesperson() {
        const order = this.pos.get_order();
        return order.sales_person_id;
    }
}
