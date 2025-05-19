/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";
// import { _t } from "@web/core/l10n/translation";
import { SalespersonList } from "../../../../salesperson_list/salesperson_list";

export class SelectSalespersonButton extends Component {
    static template = "salesperson_button_in_pos.SelectSalespersonButton";
    static props = [];

    setup() {
        this.pos = usePos();
        this.dialog = useService("dialog");
        this.state = useState({ selectedSalesPerson: null });
    }

    async selectSalesperson() {
        const currentOrder = this.pos.get_order();
        if (!currentOrder) return;

        const allSalesperson = this.pos.models["hr.employee"]?.getAll();
        
        if (!allSalesperson || allSalesperson.length === 0) {
            alert("No Salesperson Available");
            return;
        }

        this.dialog.add(SalespersonList, {
            getPayload: (selectedSalesperson) => {
                if (
                    selectedSalesperson === null ||
                    this.state.selectedSalesPerson?.id === selectedSalesperson?.id
                ) {
                    this.state.selectedSalesPerson = null;
                    currentOrder.salesperson_id = false;
                } else {
                    this.state.selectedSalesPerson = selectedSalesperson;
                    currentOrder.salesperson_id = selectedSalesperson;
                }
            },
            currentSelectedSalesperson: this.state.selectedSalesPerson || {},
        });
    }
}
