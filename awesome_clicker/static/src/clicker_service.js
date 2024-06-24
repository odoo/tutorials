/** @odoo-module **/
import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { ClickerModel } from "./clicker_model";
import { EventBus } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";
import { randomInt } from "./utils";
import { _t } from "@web/core/l10n/translation";
import { ClientAction } from "./client_action/client_action";

const commandProviderRegistry = registry.category("command_provider");

function openClientAction(action) {
    action.doAction({
        type: "ir.actions.client",
        tag: "awesome_clicker.client_action",
        target: "new",
        name: "Clicker",
    });
}

const clickerService = {
    dependencies: ["effect", "notification", "action"],
    start(_, { effect, notification, action }) {
        const clickerModel = new ClickerModel();

        clickerModel.bus.addEventListener("MILESTONE_1k", (event) => {
            console.log("HELLO FROM SERVICE");
            effect.add({
                type: "rainbow_man", // can be omitted, default type is already "rainbow_man"
                message: "Boom! You can now buy clickbots.",
            });
        });

        patch(FormController.prototype, {
            setup() {
                super.setup(...arguments);

                const percent = randomInt(100);

                // Just to debug, normally === 50
                if (percent < -1) return;
                const reward = clickerModel.getReward();
                console.log(reward);
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
            provide: (env, options) => {
                const result = [];
                result.push({
                    action() {
                        openClientAction(action);
                    },

                    category: "debug",
                    name: _t("Open Click Game"),
                });
                result.push({
                    action() {
                        clickerModel.incrementClickBots(1);
                    },

                    category: "debug",
                    name: _t("Buy 1 click bot"),
                });

                return result;
            },
        });

        return clickerModel;
    },
};

registry.category("services").add("awesome_clicker.clicker_service", clickerService);
