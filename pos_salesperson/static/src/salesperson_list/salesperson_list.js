import { Component, markRaw, useState } from "@odoo/owl";
import { Input } from "@point_of_sale/app/generic_components/inputs/input/input";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { Dialog } from "@web/core/dialog/dialog";
import { useHotkey } from "@web/core/hotkeys/hotkey_hook";
import { useService } from "@web/core/utils/hooks";
import { unaccent } from "@web/core/utils/strings";
import { SalespersonLine } from "./salesperson_line/salesperson_line";

export class SalespersonList extends Component {
    static components = { Dialog, Input, SalespersonLine };
    static template = "pos_salesperson.SalespersonList";

    static props = {
        salesperson: {
            type: [{ value: null }, Object],
            optional: true,
        },
        getPayload: { type: Function },
        close: { type: Function },
    };

    setup() {
        this.pos = usePos();
        this.ui = useState(useService("ui"));
        this.notification = useService("notification");
        this.state = useState({
            query: null,
            previousQuery: "",
            currentOffset: 0,
        });
        useHotkey("enter", () => this.onEnter());
    }

    async onEnter() {
        if (!this.state.query) {
            return;
        }
        const result = await this.searchSalesperson();
        if (result.length > 0) {
            this.notification.add(
                `${result.length} salesperson(s) found for "${this.state.query}".`,
                3000
            );
        } else {
            this.notification.add(`No more salesperson found for "${this.state.query}"`);
        }
    }

    clickSalesperson(salesperson) {
        this.props.getPayload(salesperson);
        this.props.close();
    }

    getSalespersons() {
        const searchWord = unaccent((this.state.query || "").trim(), false).toLowerCase();
        const salespersons = this.pos.models["hr.employee"].getAll();
        const numberString = searchWord.replace(/[+\s()-]/g, "");
        const isSearchWordNumber = /^[0-9]+$/.test(numberString);

        const availableSalespersons = searchWord
            ? salespersons.filter((p) =>
                unaccent(p.searchString, false).includes(isSearchWordNumber ? numberString : searchWord)
            )
            : salespersons
                .slice(0, 1000)
                .toSorted((a, b) =>
                    this.props.salesperson?.id === a.id
                        ? -1
                        : this.props.salesperson?.id === b.id
                            ? 1
                            : (a.name || "").localeCompare(b.name || "")
                );
        return availableSalespersons;
    }

    async searchSalesperson() {
        if (this.state.previousQuery != this.state.query) {
            this.state.currentOffset = 0;
        }
        const salesperson = await this.getNewSalespersons();

        if (this.state.previousQuery == this.state.query) {
            this.state.currentOffset += salesperson.length;
        } else {
            this.state.previousQuery = this.state.query;
            this.state.currentOffset = salesperson.length;
        }
        return salesperson;
    }

    async getNewSalespersons() {
        let domain = [];
        const limit = 30;
        if (this.state.query) {
            const search_fields = [
                "name",
            ];
            domain = [
                ...Array(search_fields.length - 1).fill("|"),
                ...search_fields.map((field) => [field, "ilike", this.state.query + "%"]),
            ];
        }

        const result = await this.pos.data.searchRead("hr.employee", domain, [], {
            limit: limit,
            offset: this.state.currentOffset,
        });

        return result;
    }
}
