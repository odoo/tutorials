import { _t } from "@web/core/l10n/translation";
import {
    StateSelectionField,
    stateSelectionField,
} from "@web/views/fields/state_selection/state_selection_field";
import { useCommand } from "@web/core/commands/command_hook";
import { registry } from "@web/core/registry";
import { useState } from "@odoo/owl";

export class EstateAuctionStateSelection extends StateSelectionField {
    static template = "estate_auction.EstateAuctionStateSelection";

    static props = {
        ...stateSelectionField.component.props,
        isToggleMode: { type: Boolean, optional: true },
        viewType: { type: String },
    };

    setup() {
        this.state = useState({
            isStateButtonHighlighted: false,
        });
        this.icons = {
            "template": "o_status",
            "auction": "fa fa-lg fa-gavel",
            "sold": "fa fa-lg fa-check-circle",
        };
        this.colorIcons = {
            "template": "",
            "sold": "text-success",
            "auction": "o_status_changes_requested",
        };
        this.colorButton = {
            "template": "btn-outline-secondary",
            "sold": "btn-outline-success",
            "auction": "btn-outline-warning",
        };
        if (this.props.viewType != 'form') {
            super.setup();
        } else {
            const commandName = _t("Set state as...");
            useCommand(
                commandName,
                () => {
                    return {
                        placeholder: commandName,
                        providers: [
                            {
                                provide: () =>
                                    this.options.map(subarr => ({
                                        name: subarr[1],
                                        action: () => {
                                            this.updateRecord(subarr[0]);
                                        },
                                    })),
                            },
                        ],
                    };
                },
                {
                    category: "smart_action",
                    hotkey: "alt+f",
                    isAvailable: () => !this.props.readonly && !this.props.isDisabled,
                }
            );
        }
    }

    get options() {
        return super.options;
    }

    get availableOptions() {
        return this.options;
    }

    stateIcon(value) {
        return this.icons[value] || "";
    }

    statusColor(value) {
        return this.colorIcons[value] || "";
    }

    isView(viewNames) {
        return viewNames.includes(this.props.viewType);
    }

    getDropdownPosition() {
        if (this.isView(['kanban', 'list', 'form']) || this.env.isSmall) {
            return '';
        }
        return 'bottom-end';
    }

    getTogglerClass(currentValue) {
        if (this.isView(['activity', 'kanban', 'list', 'calendar']) || this.env.isSmall) {
            return 'btn btn-link d-flex p-0';
        }
        return 'o_state_button btn rounded-pill ' + this.colorButton[currentValue];
    }

    async updateRecord(value) {
        const result = await super.updateRecord(value);
        this.state.isStateButtonHighlighted = false;
        if (result) {
            return result;
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

export const estateAuctionStateSelection = {
    ...stateSelectionField,
    component: EstateAuctionStateSelection,
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

registry.category("fields").add("estate_auction_state_selection", estateAuctionStateSelection);
