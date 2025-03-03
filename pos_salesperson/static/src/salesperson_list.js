import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import { SalespersonLine } from "@pos_salesperson/salesperson_line";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { Input } from "@point_of_sale/app/generic_components/inputs/input/input";
import { Component, useState } from "@odoo/owl";
import { useHotkey } from "@web/core/hotkeys/hotkey_hook";

export class SalespersonList extends Component {
    static components = { SalespersonLine, Dialog, Input };
    static template = "point_of_sale.SalespersonList";
    static props = {
        salesperson: {
            optional: true,
            type: [{ value: null }, Object],
        },
        getPayload: { type: Function },
        close: { type: Function },
    };

    setup() {
        this.pos = usePos();
        this.ui = useState(useService("ui"));
        this.notification = useService("notification");
        this.dialog = useService("dialog");

        this.state = useState({
            query: null,
            previousQuery: "",
            currentOffset: 0,
        });
        useHotkey("enter", () => this.onEnter());
    }
    async editSalesperson(p = false) {
        const salesperson = await this.pos.editSalesperson(p);
        if (salesperson) {
            this.clickSalesperson(salesperson);
        }
    }
    confirm() {
        this.props.resolve({ confirmed: true, payload: this.state.selectedSalesperson });
        this.pos.closeTempScreen();
    }
    
    getSalesperson() {
        const salespersons = this.pos.models["hr.employee"].getAll();
        return salespersons;
    }
    get isBalanceDisplayed() {
        return false;
    }
    clickSalesperson(salesperson) {
        this.props.getPayload(salesperson);
        this.props.close();
    }
}
