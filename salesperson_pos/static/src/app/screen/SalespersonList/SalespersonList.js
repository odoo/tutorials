import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { fuzzyLookup } from "@web/core/utils/search";
import { Dialog } from "@web/core/dialog/dialog";
import { SalespersonLine } from "./SalespersonLine/SalespersonLine";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { Input } from "@point_of_sale/app/generic_components/inputs/input/input";
import { Component, useState } from "@odoo/owl";
import { useHotkey } from "@web/core/hotkeys/hotkey_hook";
import { unaccent } from "@web/core/utils/strings";
import { makeActionAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";

export class SalespersonList extends Component {
    static components = { SalespersonLine, Dialog, Input };
    static template = "salesperson_pos.SalespersonList";
    static props = {
        salesperson: { type: [{ value: null }, Object], optional: true },
        getPayload: { type: Function },
        close: { type: Function },
    };

    setup() {
        this.pos = usePos();
        this.ui = useState(useService("ui"));
        this.notification = useService("notification");
        this.dialog = useService("dialog");
        this.action = useService("action");

        this.state = useState({
            query: "",
            previousQuery: "",
            currentOffset: 0,
            salespeople: [],
        });

        useHotkey("enter", () => this.onEnter());

        this.loadSalespeople();
    }

    async loadSalespeople() {
        this.state.salespeople = await this.getNewSalespeople();
    }

    async editSalesperson(salesperson = false) {
        try {
            const actionProps = salesperson && salesperson.id ? { resId: salesperson.id } : {};
            await makeActionAwaitable(this.action, "salesperson_pos.action_open_simplified_employee_form", { props: actionProps });
            this.loadSalespeople();
            this.props.close();
        } catch (error) {
            console.error("Error opening salesperson form:", error);
        }
    }

    getFilteredSalespeople() {
        const searchWord = unaccent((this.state.query || "").trim(), false);
        if (!searchWord) return this.state.salespeople;

        return fuzzyLookup(searchWord, this.state.salespeople, (sp) => unaccent(sp.name || "", false));
    }

    clickSalesperson(salesperson) {
        this.props.getPayload(salesperson);
        this.props.close();
    }

    async getNewSalespeople() {
        const employees = this.pos.models["hr.employee"]?.getAll() || [];

        if (this.state.query) {
            const searchWord = unaccent(this.state.query.trim().toLowerCase(), false);
            return employees.filter((employee) =>
                employee.name?.toLowerCase().includes(searchWord)
            );
        }

        return employees;
    }
}
