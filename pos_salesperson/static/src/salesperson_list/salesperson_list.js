import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { Component, useState } from "@odoo/owl";
import { useHotkey } from "@web/core/hotkeys/hotkey_hook";


export class SalespersonList extends Component {
    static template = "POS_Salesperson.SalespersonList";
    static components = { Dialog };
    static props = {
        salesperson: {
            optional: true,
            type: [{ value: null }, Object],
        },
        getPayload : { type: Function },
        close : { type: Function }
    }

    setup() {
        this.pos = usePos();
        this.ui = useState(useService("ui"));
        this.dialog = useService("dialog");

        this.state = useState({
            query: null,
            previousQuery: "",
            currentOffset: 0,
        });
        useHotkey("enter", () => this.onEnter());
    }
    getSalesPerson(){
        const salesperson = this.pos.models['hr.employee'].getAll();
        return salesperson;
    }

    clickSalesPerson(salesperson) {
        this.props.getPayload(salesperson);
        this.props.close();
    }
}
