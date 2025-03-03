import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";
import { SelectionPopup } from "@point_of_sale/app/utils/input_popups/selection_popup";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";

export class SelectSalespersonButton extends Component {
    static template = "pos_salesperson_assignment.SelectSalespersonButton";

    setup() {
        this.pos = usePos();
        this.dialog = useService("dialog");
        this.order = this.pos.get_order();
    }

    _prepareEmployeeList() {
        const employeeList = this.pos.models['hr.employee'].map((employee) => {
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
        const employeesList = this._prepareEmployeeList();
    
        if (!employeesList.length) {
            this.dialog.add(ConfirmationDialog, {
                title: _t("No Salespersons Available"),
                body: _t("There are no available salespersons to assign."),
                confirmText: _t("OK"),
            });
            return;
        }
    
        const sales_person = await makeAwaitable(this.dialog, SelectionPopup, {
            title: _t("Select Sales Person"),
            list: employeesList
        });
    
        if (sales_person) {
            this.order.setSalesPerson(sales_person);
        }        
    }

    onRemove() {
        this.order.setSalesPerson(false);
    }
    
    get salesperson() {
        return this.order.sales_person_id;
    }
}
