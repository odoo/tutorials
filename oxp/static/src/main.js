import {whenReady} from "@odoo/owl";
import {mountComponent} from "@web/env";
import {WebClient} from "./webclient";

const config = {
    dev: true,
    name: "OXP Tutorial",
};

whenReady(
    () => mountComponent(WebClient, document.body, config)
);
