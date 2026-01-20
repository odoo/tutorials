/** @odoo-module **/

import { useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";
import { browser } from "@web/core/browser/browser";
import { FormController } from "@web/views/form/form_controller";
import { ClickerModel } from "./clicker_model";

export const clickerService = {
    dependencies: ["effect"],
    start(env, services) {
        const model = new ClickerModel(JSON.parse(browser.localStorage.getItem("clicker") || '{}'));
        model.bus.addEventListener("MILESTONE_1k", () => {
            services.effect.add({
                message: "Milestone reached! You can now buy click-bots",
            });
        });
        browser.setInterval(
            () => browser.localStorage.setItem("clicker", JSON.stringify(model)),
            10 * 1000,
        );
        return model;
    }
};

export function useClicker() {
    return useState(useService("awesome_clicker.ClickerService"));
}

patch(FormController.prototype, {
    setup() {
        super.setup(...arguments);
        if (Math.random() < 0.1) {
            const clicker = useService("awesome_clicker.ClickerService");
            const reward = clicker.giveReward();
            const actionService = useService("action");
            const close = useService("notification").add(reward.description, {
                buttons: [{
                    name: "Collect",
                    onClick: () => {
                        reward.apply(clicker);
                        actionService.doAction({
                            type: "ir.actions.client",
                            tag: "awesome_clicker.ClickerClientAction",
                            target: "new",
                            name: "Clicker Game",
                        });
                        close();
                    }
                }],
            });
        }
    }
});

registry.category("services").add("awesome_clicker.ClickerService", clickerService);

registry.category("command_provider").add("clicker", {
    provide: (env, options) => {
        const clickerService = env.services["awesome_clicker.ClickerService"];
        const actionService = env.services["action"];
        return [
            {
                action() {
                    actionService.doAction({
                        type: "ir.actions.client",
                        tag: "awesome_clicker.ClickerClientAction",
                        target: "new",
                        name: "Clicker Game",
                    });
                },
                name: "Open Clicker Game",
            },
            ...clickerService.bots.filter((bot) => {
                return clickerService.checkBuyBot(bot);
            }).map((bot) => {
                return {
                    action() {
                        clickerService.buyBot(bot)
                    },
                    name: "Buy 1 " + bot.name,
                };
            }),
        ];
    },
});
