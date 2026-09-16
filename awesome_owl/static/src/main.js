import { whenReady } from "@odoo/owl";
import { mountComponent } from "@web/env";
import { Playground } from "./playground";

// config contains options used when mounting the component
const config = {
    dev: true,
    name: "Owl Tutorial" 
};

// Mount the Playground component when the document.body is ready
// mountComponent will receive these 3 - mount playground component, mount it inside browser's body, give the component its configuration
whenReady(() => mountComponent(Playground, document.body, config));

// whenReady - lets you execute something when the doc is ready
// @odoo/owl - odoo's JS module name
// mountComponent - mounts the owl component into web page
// @web/env - odoo's web module
