/** @odoo-module **/

import { registry } from "@web/core/registry";
import { StateSelectionField, stateSelectionField } from "@web/views/fields/state_selection/state_selection_field";

export class AuctionStatusSelection extends StateSelectionField {
    setup() {
        super.setup();
    }

    statusColor(value) {
        const colorMap = {
            'template': 'bg-info',
            'auction': 'bg-warning',
            'sold': 'bg-success'
        };
        return colorMap[value] || 'bg-secondary';
    }

    get label() {
        const currentValue = this.props.record.data[this.props.name];
        const currentOption = this.options.find(opt => opt[0] === currentValue);
        return currentOption ? currentOption[1] : currentValue;
    }
}

export const auctionStatusSelection = {
    ...stateSelectionField,
    component: AuctionStatusSelection
};

registry.category("fields").add("auction_status_selection", auctionStatusSelection);
