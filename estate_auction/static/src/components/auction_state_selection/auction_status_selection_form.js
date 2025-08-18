/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { StateSelectionField, stateSelectionField } from "@web/views/fields/state_selection/state_selection_field";
import { formatSelection } from "@web/views/fields/formatters";
import { registry } from "@web/core/registry";

export class AuctionStatusSelection extends StateSelectionField {
    static template = "estate_auction.AuctionStatusSelection";
    static props = {
        ...stateSelectionField.component.props,
        isToggleMode: { type: Boolean, optional: true },
        viewType: { type: String },
    };

    setup() {
        super.setup();

        const statusMap = [
            ["template", "circle", "info"],
            ["auction", "exclamation-circle", "warning"],
            ["sold", "check-circle", "success"]
        ];

        this.icons = {};
        this.colorIcons = {};
        this.colorButton = {};

        statusMap.forEach(([status, icon, color]) => {
            this.icons[status] = `fa fa-lg fa-${icon} me-2`;
            this.colorIcons[status] = `text-${color}`;
            this.colorButton[status] = `btn-outline-${color}`;
        });
    }

    get options() {
        return [["template", "Template"], ["auction", "Auction Started"], ["sold", "Sold"]];
    }

    get label() { return formatSelection(this.currentValue, { selection: this.options }); }
    stateIcon(value) { return this.icons[value] || ""; }
    statusColor(value) { return this.colorIcons[value] || ""; }
    get isToggleMode() { return this.props.isToggleMode; }

    isView(viewNames) { return viewNames.includes(this.props.viewType); }

    getTogglerClass(currentValue) {
        return (this.isView(['activity', 'kanban', 'list', 'calendar']) || this.env.isSmall)
            ? 'btn btn-link d-flex p-0'
            : 'o_state_button btn rounded-pill ' + this.colorButton[currentValue];
    }
}

export const auctionStatusSelection = {
    ...stateSelectionField,
    component: AuctionStatusSelection,
    supportedOptions: [
        ...stateSelectionField.supportedOptions,
        { label: _t("Is toggle mode"), name: "is_toggle_mode", type: "boolean" }
    ],
    extractProps({ options, viewType }) {
        const props = stateSelectionField.extractProps(...arguments);
        props.isToggleMode = Boolean(options.is_toggle_mode);
        props.viewType = viewType;
        return props;
    },
};

registry.category("fields").add("auction_status_selection_form", auctionStatusSelection);
