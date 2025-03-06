import { Component, useState } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";
import { SelectionPopup } from "@point_of_sale/app/utils/input_popups/selection_popup";
import { _t } from "@web/core/l10n/translation";

export class SelectSalesPersonButton extends Component {
    static template = "pos_salesperson.SelectSalesPersonButton";
    static props = [];

    setup() {
        this.pos = usePos();
        this.dialog = useService("dialog");
        this.state = useState({selectedSalesPerson: ""});
    }
    
    async selectSalesPerson() {
        const currentOrder = this.pos.get_order();
        if (!currentOrder) {
            return;
        }
        if (!this.pos.models || !this.pos.models["hr.employee"]) {
            return;
        }
        const allsalesperson = this.pos.models?.["hr.employee"];

        if (!allsalesperson?.length) {
            this.dialog.add(AlertDialog, {
                title: _t("No Salesperson Available"),
                body: _t("There are no available salespersons to select."),
            });
            return;
        }
        const selectedSalesPerson = await makeAwaitable(this.dialog, SelectionPopup, {
            title: _t("Select Salesperson"),
            list: this.prepareList(allsalesperson),
        });

        if (selectedSalesPerson) {
            this.state.selectedSalesPerson = selectedSalesPerson;
            currentOrder.sales_person_id = selectedSalesPerson;
        } else {
            currentOrder.selectedSalesPerson = false;
        }
    }

    prepareList = (allsalesperson) => {
        return allsalesperson.map((salesperson) => {
            return {
                id: salesperson.id,
                item: salesperson,
                label: salesperson.name,
                isSelected: false,
            };
        });
    };
}
