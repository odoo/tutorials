import { _t } from "@web/core/l10n/translation";
import { StateSelectionField, stateSelectionField } from "@web/views/fields/state_selection/state_selection_field";
import { formatSelection } from "@web/views/fields/formatters";
import { registry } from "@web/core/registry";
import { useState } from "@odoo/owl";


export class AuctionStateSelection extends StateSelectionField {
    static template = "estate_auction.AuctionStateSelection";

    static props = {
        ...stateSelectionField.component.props,
        isToggleMode: { type: Boolean, optional: true },
        viewType: { type: String },
    };

    setup() {
        this.state = useState({
            isStateButtonHighlighted: true,
        });
        this.icons = {
            "template": "o_status",
            "auction": "fa fa-lg fa-exclamation-circle",
            "sold": "o_status o_status_green"
        };
        this.colorIcons = {
            "template": "",
            "auction": "o_status_changes_requested",
            "sold": "text-success"
        };
        this.colorButton = {
            "template": "btn-outline-secondary",
            "auction": "btn-outline-warning",
            "sold": "btn-outline-success"
        };
    }

    get options() {
        return super.options;
    }

    get availableOptions() {
        return this.options;
    }

    get label() {
        const fullSelection = [...this.options];
        return formatSelection(this.currentValue, {
            selection: fullSelection,
        });
    }

    stateIcon(value) {
        return this.icons[value] || "";
    }

    statusColor(value) {
        return this.colorIcons[value] || "";
    }

    get isToggleMode() {
        return this.props.isToggleMode;
    }

    isView(viewNames) {
        return viewNames.includes(this.props.viewType);
    }

    getDropdownPosition() {
        if (this.isView(['kanban', 'list']) || this.env.isSmall) {
            return '';
        }
        return 'bottom-end';
    }

    getTogglerClass(currentValue) {
        return this.isView(['kanban', 'list']) || this.env.isSmall
            ? 'btn btn-link d-flex p-0'
            : `o_state_button btn rounded-pill ${this.colorButton[currentValue]}`;
    }

    async updateRecord(value) {
        try {
            const result = await super.updateRecord(value);
            this.state.isStateButtonHighlighted = false;
            return result;
        } catch (error) {
            console.error("Failed to update state:", error);
            this.env.services.notification.add(_t("Failed to update state."), {
                type: "danger",
            });
        }
    }

    onMouseEnterStateButton(ev) {
        if (!this.env.isSmall) {
            this.state.isStateButtonHighlighted = true;
        }
    }

    onMouseLeaveStateButton(ev) {
        this.state.isStateButtonHighlighted = false;
    }
}

export const auctionStateSelection = {
    ...stateSelectionField,
    component: AuctionStateSelection,
    supportedOptions: [
        ...stateSelectionField.supportedOptions, {
            label: _t("Is toggle mode"),
            name: "is_toggle_mode",
            type: "boolean"
        }
    ],
    extractProps({ options, viewType }) {
        const props = stateSelectionField.extractProps(...arguments);
        props.isToggleMode = Boolean(options.is_toggle_mode);
        props.viewType = viewType;
        return props;
    },
}

registry.category("fields").add("auction_state_selection", auctionStateSelection);
