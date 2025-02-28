import { useState } from "@odoo/owl";

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

import  { ClickerModel } from "./clicker_model"

export function useClicker() {
    return useState(useService("awesome_clicker.clicker_service"));
}

export const clickerService = {
    dependencies: ["effect"],
    start(env, services) {
        const clicker = new ClickerModel();
        clicker.bus.addEventListener("MILESTONE_1k", () => {
            services.effect.add({
                type: "rainbow_man",
                message: "Milestone reached! You can now buy clickbots",
            });
        });
        clicker.bus.addEventListener("MILESTONE_5k", () => {
            services.effect.add({
                type: "rainbow_man",
                message: "Milestone reached! You can now buy BIG bots",
            });
        });

        return clicker;
    }
}

registry.category("services").add("awesome_clicker.clicker_service", clickerService)

registry.category("command_provider").add("awesome_clicker", {
    dependencies: ["action", "awesome_clicker.clicker_service"], // unsure if it works since action and clicker is in a different subregistry
    provide: (env, options) => {
        let commands = [
            {
                category: "awesome_clicker",
                name: "Open Clicker Game",
                action() {
                    env.services.action.doAction({
                        type: 'ir.actions.client',
                        name: 'Clicker',
                        tag: 'awesome_clicker.client_action',
                        target: 'new'
                    });
                }
            }
        ]
        const clicker = env.services['awesome_clicker.clicker_service'];
        if (clicker.level >= 1 && clicker.clicks >= 1000) {
            commands.push({
                category: "awesome_clicker",
                name: "Buy 1 click bot",
                action() {
                    clicker.buyBot();
                }
            })
        }
        return commands;
    }
})
