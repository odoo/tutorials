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
        const salesperson = this.pos.get_order()?.getSalesperson();
        if (salesperson) {
            this.props.salesperson = salesperson;
        }
    }

    async selectSalesperson(){
        const currentOrder = this.pos.get_order();
        if (!currentOrder) return;
        const salesperson_list = this.pos.models['hr.employee'].map((sp) => {
            return {
                id: sp.id,
                item: sp,
                label: sp.name,
                isSelected: currentOrder.getSalesperson()?.id === sp.id
            }
        });
        const selectedSalesperson = await makeAwaitable(this.dialog, SelectionPopup, {
            title: _t("Select salesperson"),
            list: salesperson_list,
        });
        if (selectedSalesperson) return;
        const same = currentOrder.getSalesperson()?.id === selected.id;
        this.props.salesperson = same ? null : selected;
        order.setSalesperson(same ? "" : selected);
    }
}
