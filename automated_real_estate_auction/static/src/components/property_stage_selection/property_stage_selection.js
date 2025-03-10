import { useState } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { useCommand } from "@web/core/commands/command_hook";
import { registry } from "@web/core/registry";
import { formatSelection } from "@web/views/fields/formatters";
import {
    StateSelectionField,
    stateSelectionField,
} from "@web/views/fields/state_selection/state_selection_field";

export class PropertyAuctionStageSelection extends StateSelectionField {
    static template = "automated_real_estate_auction.PropertyAuctionStageSelection";

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
            "auction": "fa fa-gavel",
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
        if (this.props.viewType !== 'form') {
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
                                    this.options.length
                                        ? this.options.map(subarr => ({
                                              name: subarr[1],
                                              action: () => {
                                                  this.updateRecord(subarr[0]);
                                              },
                                          }))
                                        : [],
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

export const propertyAuctionStageSelection = {
    ...stateSelectionField,
    component: PropertyAuctionStageSelection,
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

registry.category("fields").add("property_stage_selection", propertyAuctionStageSelection);
