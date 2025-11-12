import { whenReady } from "@odoo/owl";
import { mountComponent } from "@web/env";
import { Playground } from "./playground";

const config = {
    dev: true,
    name: "Owl Tutorial",
};

whenReady(() => mountComponent(Playground, document.body, config));
