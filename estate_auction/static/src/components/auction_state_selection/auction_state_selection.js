/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import {
    StateSelectionField,
    stateSelectionField,
} from "@web/views/fields/state_selection/state_selection_field";
import { useCommand } from "@web/core/commands/command_hook";
import { formatSelection } from "@web/views/fields/formatters";

import { registry } from "@web/core/registry";
import { useState } from "@odoo/owl";


export class AuctionStateSelection extends StateSelectionField {
    static template = "estate.AuctionStateSelection";

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
            "auction": "fa fa-lg fa-exclamation-circle",
            "sold": "fa fa-lg fa-circle",
        };
        this.colorIcons = {
            "template": "",
            "auction": "o_status_changes_requested",
            "sold": "text-success",
        };
        this.colorButton = {
            "template": "btn-outline-secondary",
            "auction": "btn-outline-warning",
            "sold": "btn-outline-success",
        };
        if (this.props.viewType != 'form') {
            super.setup();
        } else {
            const commandName = _t("Set auction state as...");
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
        const labels = new Map(super.options);
        const states = ["canceled", "sold"];
        const currentState = this.props.record.data[this.props.name];
        if (currentState != "waiting") {
            states.unshift("template", "auction");
        }
        return states.map((state) => [state, labels.get(state)]);
    }

    get availableOptions() {
        // overrided because we need the currentOption in the dropdown as well
        return this.options;
    }

    get label() {
        const waitOption = super.options.find(([state, _]) => state === "waiting");
        const fullSelection = [...this.options];
        if (waitOption) {
            fullSelection.push(waitOption);
        }
        return formatSelection(this.currentValue, {
            selection: fullSelection,
        });
    }

    stateIcon(value) {
        return this.icons[value] || "";
    }

    /**
     * @override
     */
    statusColor(value) {
        return this.colorIcons[value] || "";
    }

    /**
     * determine if a single click will trigger the toggleState() method
     * which will switch the state from auction to sold.
     */
    get isToggleMode() {
        return this.props.isToggleMode;
    }

    isView(viewNames) {
        return viewNames.includes(this.props.viewType);
    }

    async toggleState() {
        const toggleVal = this.currentValue == "sold" ? "auction" : "sold";
        await this.updateRecord(toggleVal);
    }

    getDropdownPosition() {
        if (this.isView(['activity', 'kanban', 'list', 'calendar']) || this.env.isSmall) {
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

    /**
     * @param {MouseEvent} ev
     */
    onMouseEnterStateButton(ev) {
        if (!this.env.isSmall) {
            this.state.isStateButtonHighlighted = true;
        }
    }

    /**
     * @param {MouseEvent} ev
     */
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
