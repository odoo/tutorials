import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { clickerModel } from "./clicker_model";
import { browser } from "@web/core/browser/browser";
import { migration } from "./migration";

export const state = reactive({ clicks: 0, level: 1, clickBots: 0 });

export const clickerService = {
    start() {

        const model = reactive (new clickerModel);
        const game_save = JSON.parse(browser.localStorage.getItem("game_save"));
        if (!game_save) {
            browser.localStorage.setItem("game_save", JSON.stringify(model.getModelStatus()));
        } else {
            if (game_save.version < 3){
                for (let i = 0; i++; i<migration.length){
                    if (migration[i].fromVersion = game_save.version ){
                        game_save = migration[i].apply(game_save);
                        break
                    }
                }
            }
            model.setModelStatus(game_save);
        }

        // browser.localStorage.removeItem("game_save");

        const save = () => {
            browser.localStorage.setItem("game_save", JSON.stringify(model.getModelStatus()));
        }
        browser.setInterval(save, 10 * 1000);

        return model;
    }
};


registry.category("services").add("awesome_clicker.clicker_service", clickerService);