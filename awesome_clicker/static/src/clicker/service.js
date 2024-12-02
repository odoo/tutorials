import {reactive} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {GAME_DATA} from "./data";
import {loadGame, saveGame} from "./save";

const clickerService = {
    dependencies: ['effect'],

    start(env, {effect}) {

        const store = reactive(loadGame(), () => saveGame(store));
        saveGame(store)

        store.bus.addEventListener("ACHIEVEMENT", (ev) => {
            effect.add({
                message: `Milestone reached! You can now buy ${ev.detail.unlock}`,
                type: 'rainbow_man'
            })
        })

        store.bus.addEventListener("LEVEL", (ev) => {
            effect.add({
                message: `Level ${ev.detail.level} reached! ${ev.detail.message}`,
                type: 'rainbow_man'
            })
        })

        //useExternalListener(document.body, "click", this.increment, {});

        setInterval(() => {
            store.tick()
        }, GAME_DATA.tick);

        return store
    }
}

registry.category("services").add("awesome_clicker.clicker", clickerService);