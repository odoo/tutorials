/** @odoo-module **/

import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";
import { SelectionPopup } from "@point_of_sale/app/utils/input_popups/selection_popup";

export class SelectSalespersonButton extends Component {
    static template = "point_of_sale.SelectSalespersonButton";
    static props = ["salesperson?"]

    setup() {
        this.pos = usePos();
        this.dialog = useService("dialog");
        const currentOrder = this.pos.get_order();
        if (currentOrder) {
            const currentSalesperson = currentOrder.getSalesperson();
            if (currentSalesperson) {
                this.props.salesperson = currentSalesperson;
            }
            else{
                return;
            }
        }
    }

    async selectSalesperson(){
        const currentOrder = this.pos.get_order();
        if (!currentOrder) {
            return false;
        }
        const salesperson_list = this.pos.models['hr.employee'].map((sp) => {
            return {
                id: sp.id,
                item: sp,
                label: sp.name,
                isSelected: currentOrder.getSalesperson()?.id === sp.id || false 
            }
        });
        console.log(this.pos.models['hr.employee'].getAll());
        const selectedSalesperson = await makeAwaitable(this.dialog, SelectionPopup, {
            title: _t("Select salesperson"),
            list: salesperson_list,
        });

        if (selectedSalesperson) {
            if (currentOrder.getSalesperson()?.id === selectedSalesperson.id) {
                this.props.salesperson = null;
                currentOrder.setSalesperson("");
            }
            else {
                this.props.salesperson = selectedSalesperson;
                currentOrder.setSalesperson(selectedSalesperson);
            }
        }
        else{
            return;
        }
    }
}
