import { Component, useState, useExternalListener, markup } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { useClicker } from "../clicker_hook";
import { ClickValue } from "../click_value";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";

import { FormController } from "@web/views/form/form_controller";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";

export class ClickerSystrayItem extends Component {
    static template = "clicker_systray_item.ClickerSystrayItem";
    static props = {};
    static components = { ClickValue, Dropdown, DropdownItem };

    setup() {
        this.action = useService("action");
        this.state = useClicker();
        this.effect = useService("effect");
        useExternalListener(window, "click", () => {
            this.state.increment(1);
        })
        this.state.bus.addEventListener("MILESTONE_1k", () => {
            this.effect.add({
                type: "rainbow_man", // can be omitted, default type is already "rainbow_man"
                message: "Boom! Team record for the past 30 days.",
            });
        });
        const commandProviderRegistry = registry.category("command_provider");
        commandProviderRegistry.add("commandClickerGame", {
            provide: (env, options = {}) => {
                const commands = [];
                commands.push({
                    action: () => { this.open_client_action(); },
                    name: "Open Clicker Game",
                });
                commands.push({
                    action: () => {
                        if (this.state.clicks >= 1000) {
                            this.state.incrementClickBots(1);
                        }
                    },
                    name: "Buy 1 click bot"

                })
                return commands;
            }
        })
    }

    increment_button(event) {
        event.stopPropagation();
        this.state.increment(10);
    }

    increment_clickbot() {
        if (this.state.clicks >= 1000) {
            this.state.incrementClickBots(1);
        }
    }

    open_client_action() {
        this.action.doAction(
            {
                type: "ir.actions.client",
                tag: "awesome_clicker.client_action",
                target: "new",
                name: "Clicker"
            });
    }

}


const systrayItem = {
    Component: ClickerSystrayItem
}

registry.category("systray").add("clicker.systrayItem", systrayItem);


patch(FormController.prototype, {
    setup() {
        super.setup(...arguments)
        this.clicks = useClicker();
        this.notification = useService("notification");
        this.action = useService("action");

        const applyAndAction = (reward) => {
            this.clicks.applyReward(reward);
            this.action.doAction(
                {
                    type: "ir.actions.client",
                    tag: "awesome_clicker.client_action",
                    target: "new",
                    name: "Clicker"
                }
            )
        }

        // if (Math.random() < 0.001){
        if (Math.random() < 0.98) {
            let reward = this.clicks.getReward();
            const closeFn = this.notification.add(
                _t('Congrats you won a reward: "%s"', reward.description),
                {
                    sticky: true,
                    type: "success",
                    buttons: [{
                        name: "collect",
                        onClick: () => { applyAndAction(reward); closeFn(); }
                    }]
                }
            );
        }
    }
})