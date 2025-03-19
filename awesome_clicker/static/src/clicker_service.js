import { useState } from "@odoo/owl";

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { browser } from "@web/core/browser/browser";

import  { ClickerModel } from "./clicker_model"

export function useClicker() {
    return useState(useService("awesome_clicker.clicker_service"));
}

export const clickerService = {
    dependencies: ["effect"],
    start(env, services) {
        const clicker = new ClickerModel();
        const data = JSON.parse(browser.localStorage.getItem("awesome_clicker.clicker"));
        if (data) {
            Object.assign(clicker, data);
        }

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

        setInterval(() => {
            clicker.increment((clicker.clickerBots * 10 + clicker.clickerBigBots * 100) * clicker.power);
            browser.localStorage.setItem("awesome_clicker.clicker", JSON.stringify(clicker, (key, value) => {if (key === "bus") {return undefined} return value}));
        }, 10000);

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
