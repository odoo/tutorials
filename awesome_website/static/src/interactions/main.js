import { registry } from "@web/core/registry";
import { Interaction } from "@web/public/interaction";

class Main extends Interaction {
    /* Interaction's lifecycle methods:

    setup() { }
    async willStart() { }
    start() { }
    destroy() { }

    */
}

registry.category("public.interactions").add("awesome_website.main", Main);
