import { whenReady } from "@odoo/owl";
import { mountComponent } from "@web/env";
import {Playground} from "./playground"

const config = {
    dev: true,
    name: "Supplier Portal",
};

whenReady(() => mountComponent(Playground, document.body, config));
