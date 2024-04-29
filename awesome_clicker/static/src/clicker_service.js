/** @odoo-module **/

import { EventBus } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { ClickerModel } from "./clicker_model";
import { FormController } from "@web/views/form/form_controller";
import { patch } from "@web/core/utils/patch";
import { browser } from "@web/core/browser/browser";

const current_version = 1.3

const migrations = [
    {
        fromVersion: 1.0,
        toVersion: 1.1,
        apply(state) {
            console.log(state)
        }
    },
    {
        fromVersion: 1.1,
        toVersion: 1.2,
        apply(state) {
            console.log(state)
        }
    },
    {
        fromVersion: 1.2,
        toVersion: 1.3,
        apply(state) {
            console.log(state)
        }
    },
];

function toCurrentVersion(save) {
    if (save.version > current_version)
        return
    while (save.version != current_version)
        for (const migration of migrations)
            if (migration.fromVersion == save.version)
                migrateSave(save, migration);
}

function migrateSave(save, migration) {
    console.log("migrating")
    console.log(save)
    console.log(migration)
    save.version = migration.toVersion;
    console.log("Before", save.state)
    migration.apply(save.state)
    console.log("After", save.state)
}

const clickerService = {
    dependencies: ["effect", "notification", "action"],
    start(_env, { effect, notification, action }) {
        const bus = new EventBus();
        const clicker = new ClickerModel(bus, notification, action);

        var save = JSON.parse(browser.localStorage.getItem("clicker"));
        toCurrentVersion(save);
        clicker.loadState(save.state);
    
        patch(FormController.prototype, {
            setup() {
                super.setup(...arguments);
                this.clicker = clicker;
                this.clicker.getReward();
            }
        });
        
        setInterval(() => {
            browser.localStorage.setItem("clicker", JSON.stringify({version: current_version, state: clicker.getState()}));
        }, 1_000);

        const commandProviderRegistry = registry.category("command_provider");
        commandProviderRegistry.add("clicker", {
            provide: (env, options) => {
                const result = [];

                result.push({
                    action() {
                        action.doAction({
                            type: "ir.actions.client",
                            tag: "awesome_clicker.client_action",
                            target: "new",
                            name: "Clicker"
                        });
                    },
                    category: "clicker",
                    name: "Open Clicker Game",
                });
                result.push({
                    action() {
                        clicker.buyClickBot()
                    },
                    category: "clicker",
                    name: "Buy 1 click bot",
                });
                
                return result;
            },
        });

        bus.addEventListener("MILESTONE_1k", () => {
            effect.add({
                type: "rainbow_man",
                message: "Milestone reached! You can now buy click bots.",
            });
        });
        bus.addEventListener("MILESTONE_5k", () => {
            effect.add({
                type: "rainbow_man",
                message: "Milestone reached! You can now buy big bots.",
            });
        });
        bus.addEventListener("MILESTONE_100k", () => {
            effect.add({
                type: "rainbow_man",
                message: "Milestone reached! You can now buy power.",
            });
        });
        bus.addEventListener("MILESTONE_1m", () => {
            effect.add({
                type: "rainbow_man",
                message: "Milestone reached! You can now buy trees.",
            });
        });

        return clicker;
    }
}

registry.category("services").add("clicker", clickerService);
