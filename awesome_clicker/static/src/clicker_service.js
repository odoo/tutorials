/** @odoo-module **/

import { registry } from "@web/core/registry";
import { clickerBus, ClickerModel } from "./clicker_model";
import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";
import { migrationUpdate, randomInt } from "./utils";
import { _t } from "@web/core/l10n/translation";
import { browser } from "@web/core/browser/browser";
import { migrations } from "./clicker_model_migrations";

const commandProviderRegistry = registry.category("command_provider");

function openClientAction(action) {
    action.doAction({
        type: "ir.actions.client",
        tag: "awesome_clicker.client_action",
        target: "new",
        name: "Clicker",
    });
}

function handleNewVersion(clickerModel) {
    const oldClickerModel = browser.localStorage.getItem("clickerState");
    if (!oldClickerModel) return;
    const parsedModel = JSON.parse(oldClickerModel);
    const newVersion = clickerModel.versionNumber;
    Object.assign(clickerModel, parsedModel);
    clickerModel.versionNumber = newVersion;
    migrationUpdate(migrations, clickerModel, parsedModel.versionNumber, clickerModel.versionNumber);
}

const clickerService = {
    dependencies: ["effect", "notification", "action"],
    start(_, { effect, notification, action }) {
        const clickerModel = new ClickerModel();
        handleNewVersion(clickerModel);

        setInterval(() => browser.localStorage.setItem("clickerState", JSON.stringify(clickerModel)), 10 * 1000);

        clickerBus.addEventListener("MILESTONE_1k", (_) => {
            effect.add({
                type: "rainbow_man",
                message: "Boom! You can now buy clickbots.",
            });
        });

        patch(FormController.prototype, {
            setup() {
                super.setup(...arguments);

                // Just to debug, normally === 50
                if (randomInt(100) < -1) return;

                const reward = clickerModel.getReward();
                if (!reward) return;

                notification.add(_t(`Congrats you won a reward: "${reward.description}"`), {
                    type: "success",
                    buttons: [
                        {
                            name: _t("Collect"),
                            onClick: () => {
                                reward.apply(clickerModel);
                                openClientAction(action);
                            },
                        },
                    ],
                });
            },
        });

        commandProviderRegistry.add("awesome_clicker", {
            provide: () => {
                return [
                    {
                        action() {
                            openClientAction(action);
                        },
                        category: "debug",
                        name: _t("Open Click Game"),
                    },
                    {
                        action() {
                            clickerModel.incrementClickBots();
                        },
                        category: "debug",
                        name: _t("Buy 1 click bot"),
                    },
                ];
            },
        });

        return clickerModel;
    },
};

registry.category("services").add("awesome_clicker.clicker_service", clickerService);
