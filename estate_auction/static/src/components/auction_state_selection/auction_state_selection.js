import { StateSelectionField, stateSelectionField } from "@web/views/fields/state_selection/state_selection_field";
import { useCommand } from "@web/core/commands/command_hook";
import { registry } from "@web/core/registry";
import { useState } from "@odoo/owl";

export class AuctionStateSelection extends StateSelectionField {
    static template = "estate_auction.AuctionStateSelection";

    static props = {
        ...stateSelectionField.component.props,
        viewType: { type: String },
    };

    setup() {
        this.state = useState({
            isStateButtonHighlighted: false,
        });
        
        this.icons = {
            "template": "fa fa-lg fa-file-text-o",
            "auction": "fa fa-lg fa-gavel",
            "sold": "fa fa-lg fa-check-circle",
        };

        this.colorIcons = {
            "template": "text-muted",
            "auction": "text-warning",
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
            const commandName = "Set state as...";
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

    stateIcon(value) {
        return this.icons[value] || "";
    }

    statusColor(value) {
        return this.colorIcons[value] || "";
    }

    isView(viewNames) {
        return viewNames.includes(this.props.viewType);
    }
    
    getTogglerClass(currentValue) {
        if (this.isView(['kanban', 'list']) || this.env.isSmall) {
            return 'btn btn-link d-flex p-0';
        }
        return 'o_state_button btn rounded-pill ' + this.colorButton[currentValue];
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
    extractProps({ options, viewType }) {
        const props = stateSelectionField.extractProps(...arguments);
        props.viewType = viewType;
        return props;
    },
}

registry.category("fields").add("auction_state_selection", auctionStateSelection);
