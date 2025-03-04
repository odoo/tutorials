import { _t } from "@web/core/l10n/translation";
import { Component, useState } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { SalespersonList } from "../../../salesperson_list/salesperson_list";

export class SelectSalesPersonButton extends Component {
    static template = "pos_salesperson.SelectSalesPersonButton";
    static props = [];

    setup() {
        this.pos = usePos();
        this.dialog = useService("dialog");
        this.state = useState({ selectedSalesPerson: null });
    }

    async selectSalesPerson() {
        const currentOrder = this.pos.get_order();
        if (!currentOrder) return;

        const allSalesperson = this.pos.models["hr.employee"]?.getAll();

        if (!allSalesperson?.length === 0) {
            this.dialog.add(AlertDialog, {
                title: _t("No Salesperson Available"),
                body: _t("There are no available salespersons to select."),
            });
            return;
        }

        this.dialog.add(SalespersonList, {
            close: () => {},
            getPayload: (selectedSalesperson) => {
                if (this.state.selectedSalesPerson?.id === selectedSalesperson.id) {
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
