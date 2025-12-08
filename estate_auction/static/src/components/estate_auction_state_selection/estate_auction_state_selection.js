/** @odoo-module **/

import { registry } from '@web/core/registry';
import { StateSelectionField, stateSelectionField } from '@web/views/fields/state_selection/state_selection_field';

export class EstateAuctionStateSelection extends StateSelectionField {
    static template = 'estate_auction.EstateAuctionStateSelection';
    static props = {
        ...stateSelectionField.component.props,
        viewType: {type: String}
    };

    setup() {
        this.icons = {
            '01_template': 'fa-circle-o',
            '02_auction': 'fa fa-lg fa-exclamation-circle',
            '03_sold': 'fa fa-lg fa-circle'
        };

        this.colorIcons = {
            '01_template': 'text-secondary',
            '02_auction': 'text-warning',
            '03_sold': 'text-success'
        };

        super.setup();
    }

    statusIcon(value) {
        return `fa fa-lg ${this.icons[value] || ''}`;
    }

    /**
     * @override
     */
    statusColor(value) {
        return this.colorIcons[value] || '';
    }

    statusButton(value) {
        return `btn-${this.colorIcons[value]?.split('-')[1] || 'secondary'}`;
    }

    isView(viewNames) {
        return viewNames.includes(this.props.viewType);
    }
}

export const estateAuctionStateSelection = {
    ...stateSelectionField,
    component: EstateAuctionStateSelection,
    extractProps({viewType}) {
        const props = stateSelectionField.extractProps(...arguments);
        props.viewType = viewType;
        return props;
    }
};

registry.category('fields').add('estate_auction_state_selection', estateAuctionStateSelection);
