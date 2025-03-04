import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { fuzzyLookup } from "@web/core/utils/search";
import { Input } from "@point_of_sale/app/generic_components/inputs/input/input";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { unaccent } from "@web/core/utils/strings";

export class SalespersonList extends Component {
    static template = "pos_salesperson.SalespersonList";
    static components = { Dialog, Input };
    static props = {
        close: { type: Function },
        getPayload: { type: Function },
        currentSelectedSalesperson: { type: Object },
    };

    setup() {
        this.pos = usePos();
        this.dialog = useService("dialog");
        this.allSalesperson = this.pos.models["hr.employee"]?.getAll();
        this.state = useState({ query: "", selectedSalesPerson: null });
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

    selectSalesperson(salesperson) {
        const currentOrder = this.pos.get_order();
        if (!currentOrder) return;

        this.props.getPayload(salesperson);
        this.props.close();
    }

    onSearchInput(event) {
        this.state.query = event?.target?.value;
    }
}
