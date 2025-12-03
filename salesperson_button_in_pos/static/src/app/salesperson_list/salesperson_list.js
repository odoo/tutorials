import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import { Input } from "@point_of_sale/app/generic_components/inputs/input/input";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { _t } from "@web/core/l10n/translation";
import { unaccent } from "@web/core/utils/strings";
import { fuzzyLookup } from "@web/core/utils/search";
import { useHotkey } from "@web/core/hotkeys/hotkey_hook";
import { makeActionAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";


export class SalespersonList extends Component {
    static template = "salesperson_button_in_pos.SalespersonList";
    static components = {Dialog, Input };
    static props = {
        getPayload: { type: Function },
        close: { type: Function },
        currentSelectedSalesperson: { type: Object },
    };

    setup(){
        this.pos = usePos();
        this.dialog = useService("dialog");
        this.action=useService("action");
        this.ui = useState(useService("ui"));
        this.notification = useService("notification");
        this.allSalesperson = this.pos.models["hr.employee"]?.getAll();
        this.state = useState({
            query: "",
            selectedSalesPerson: null
        });
        useHotkey("enter", () => this.onEnter());
        this.loadSalespeople();
    }

    async loadSalespeople() {
        this.state.salespeople = await this.getSalespersons();
    }

    async editSalesperson(salesperson = false) {
        try {
            const actionProps = salesperson && salesperson.id ? { resId: salesperson.id } : {};
    
            await this.env.services.action.doAction("salesperson_button_in_pos.action_salesperson_create_form_view", {
                props: actionProps,
                onClose: async () => {
                    await this.loadSalespeople(); 
                    this.props.close();             
                },
            });
        } catch (error) {
            console.error("Error opening salesperson form:", error);
        }
    }
    
    get filteredSalespersons() {
        if (!this.state.query) {
            return this.allSalesperson;
        }
        return fuzzyLookup(
            this.state.query,
            this.allSalesperson,
            (salesperson) => unaccent(salesperson.name)
        );
    }

    getSalespersons() {
        const users = this.pos.models["res.users"].getAll();
        const query = this.state.query?.toLowerCase() || "";
        return users.filter((u) => u.name?.toLowerCase().includes(query));
    }

    selectSalesperson(salesperson) {
        const currentOrder = this.pos.get_order();
        if (!currentOrder) return;

        if (this.props.currentSelectedSalesperson?.id === salesperson.id) {
            this.props.getPayload(null);
        } else {
            this.props.getPayload(salesperson);
        }
    this.props.close();
    }

    onEnter() {
        this.notification.add(_t('No more customer found for "%s".', this.state.query),300);
    }
    
    onSearchInput(event) {
        this.state.query = event?.target?.value;
    }
}
