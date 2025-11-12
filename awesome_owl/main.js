import { whenReady } from "@odoo/owl";
import { mountComponent } from "@web/env";
import { Playground } from "./playground";  // Ensure the path is correct

const config = {
    dev: true,
    name: "Owl Tutorial",
};

// Mount the Playground component to the #playground-container when the document is ready
whenReady(() => {
    const container = document.querySelector("#playground-container");
    if (container) {
        mountComponent(Playground, container, config);  // Mount the component
    }
});
