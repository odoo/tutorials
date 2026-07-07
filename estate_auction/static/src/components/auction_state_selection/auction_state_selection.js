import {
    StateSelectionField,
    stateSelectionField,
} from "@web/views/fields/state_selection/state_selection_field";

import { registry } from "@web/core/registry";


export class AuctionStateSelection extends StateSelectionField {
    static template = "estate_auction.AuctionStateSelection";

    setup() {
        super.setup();

        this.icons = {
            "template": "fa fa-circle-o",
            "auction": "fa fa-check-circle",
            "sold": "fa fa-times-circle",
        };

        this.colorIcons = {
            "template": "text-secondary",
            "auction": "text-success",
            "sold": "text-danger",
        };

        this.colorButton = {
            "template": "btn-outline-secondary",
            "auction": "btn-outline-success",
            "sold": "btn-outline-danger",
        };
    }

    stateIcon(value) {
        return this.icons[value] || "";
    }

    statusColor(value) {
        return this.colorIcons[value] || "";
    }

    getTogglerClass(currentValue) {
        return (
            "o_state_button btn rounded-pill " +
            this.colorButton[currentValue]
        );
    }
}

export const auctionStateSelection = {
    ...stateSelectionField,
    component: AuctionStateSelection,
};

registry.category("fields").add("auction_state_selection", auctionStateSelection);
