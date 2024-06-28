/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ClickerModel } from "./clicker_model";
import { browser } from "@web/core/browser/browser";

export const clickerService = {
    dependencies: ["effect", "notification", "action"],

    start(env, { effect, notification, action }) {

        const previousState = browser.localStorage.getItem("savedClickerModel")?.split(",") || [];

        for(var i=0; i<previousState.length; i++) {
            previousState[i] = Number(previousState[i]);
        }

        var clickerModel;

        if (true && previousState.length > 0) {
            clickerModel = new ClickerModel(previousState);
        } 
        else {
            clickerModel = new ClickerModel();
        }

        clickerModel.bus.addEventListener("level_1_is_reached", () => effect.add({
            message: "Level 1 is reached! You can now buy ClickBots",
            type: "rainbow_man",
        }));
        clickerModel.bus.addEventListener("level_2_is_reached", () => effect.add({
            message: "Level 2 is reached! You can now buy BigBots",
            type: "rainbow_man",
        }));
        clickerModel.bus.addEventListener("level_3_is_reached", () => effect.add({
            message: "Level 3 is reached! You can now buy some Power",
            type: "rainbow_man",
        }));
        clickerModel.bus.addEventListener("reward_obtained", (ev) => {const closeNotification = notification.add(
            ev.detail.description, {
                title: "Congrats, you won a reward!",
                sticky: true,
                buttons: [{
                    name: "Collect and Open",
                    onClick: () => {
                        ev.detail.apply(clickerModel);
                        closeNotification();
                        action.doAction({
                            type: "ir.actions.client",
                            tag: "awesome_clicker.client_action",
                            target: "new",
                            name: "Clicker Game"
                        });
                    },
                },{
                    name: "Collect",
                    onClick: () => {
                        ev.detail.apply(clickerModel);
                        closeNotification();
                    },
                },],
            }
        )});

        return clickerModel;
    },
};

registry.category("services").add("awesome_clicker.clicker", clickerService);
