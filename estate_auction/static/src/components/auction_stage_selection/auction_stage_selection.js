import { _t } from "@web/core/l10n/translation";
import {
    StateSelectionField,
    stateSelectionField,
} from "@web/views/fields/state_selection/state_selection_field";
import { useCommand } from "@web/core/commands/command_hook";
import { formatSelection } from "@web/views/fields/formatters";

import { registry } from "@web/core/registry";
import { useState } from "@odoo/owl";

export class AuctionStageSelection extends StateSelectionField {
    static template = "auction.AuctionStageSelection";

    static props = {
        ...stateSelectionField.component.props,
        viewType: { type: String },
    };

    setup() {
        this.state = useState({
            isStateButtonHighlighted: false,
        });
        this.icons = {
            "01_template": "fa fa-lg fa-file-text-o",
            "02_auction": "fa fa-lg fa-gavel",
            "03_sold": "fa fa-lg fa-check-circle",
        };
        this.colorIcons = {
            "01_template": "text-muted",
            "02_auction": "text-primary",
            "03_sold": "text-success",
        };
        this.colorButton = {
            "01_template": "btn-outline-secondary",
            "02_auction": "btn-outline-primary",
            "03_sold": "btn-outline-success",
        };
        if (this.props.viewType != 'form') {
            super.setup();
        } else {
            const commandName = _t("Set auction stage as...");
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
                    hotkey: "alt+a",
                    isAvailable: () => !this.props.readonly && !this.props.isDisabled,
                }
            );
        }
    }

    get options() {
        const labels = new Map(super.options);
        const states = ["01_template", "02_auction", "03_sold"];
        return states.map((state) => [state, labels.get(state)]);
    }

    get availableOptions() {
        return this.options;
    }

    get label() {
        return formatSelection(this.currentValue, {
            selection: this.options,
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

    isView(viewNames) {
        return viewNames.includes(this.props.viewType);
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

export const auctionStageSelection = {
    ...stateSelectionField,
    component: AuctionStageSelection,
    extractProps(...args) {
        const props = stateSelectionField.extractProps(...args);
        props.viewType = args[0].viewType;
        return props;
    },
}

registry.category("fields").add("auction_stage_selection", auctionStageSelection);

console.log("Auction Stage Selection component created");
