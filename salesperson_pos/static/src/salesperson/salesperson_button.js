/** @odoo-module **/

import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";
import { SelectionPopup } from "@point_of_sale/app/utils/input_popups/selection_popup";

export class SelectSalespersonButton extends Component {
    static template = "point_of_sale.SelectSalespersonButton";
    static props = ["salesperson?"];

    setup() {
        this.pos = usePos();
        this.dialog = useService("dialog");
        const currentOrder = this.pos.get_order();
        this.props.salesperson = currentOrder?.getSalesperson() || null;
    }

    async selectSalesperson() {
        const currentOrder = this.pos.get_order();
        if (!currentOrder) return;

        const salespeople = this.pos.models["hr.employee"] || [];
        const salespersonList = salespeople.map(sp => ({
            id: sp.id,
            item: sp,
            label: sp.name,
            isSelected: currentOrder.getSalesperson()?.id === sp.id
        }));

        const selectedSalesperson = await makeAwaitable(this.dialog, SelectionPopup, {
            title: _t("Select Salesperson"),
            list: salespersonList,
        });
        //toggleselection
        if (selectedSalesperson) {
            const isSameSelection = currentOrder.getSalesperson()?.id === selectedSalesperson.id;
            this.props.salesperson = isSameSelection ? null : selectedSalesperson;
            currentOrder.setSalesperson(isSameSelection ? "" : selectedSalesperson);
        }
    }
}
