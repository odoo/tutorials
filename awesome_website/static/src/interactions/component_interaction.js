import { registry } from "@web/core/registry";
import { Interaction } from "@web/public/interaction";
import { VeryBasicComp } from "../components/very_basic_comp";

class ComponentInteraction extends Interaction {
    static selector = "main";

    dynamicContent = {
        _root: {
            "t-component": () => [VeryBasicComp, { name: "Odooer" }],
        },
    };
}

registry
    .category("public.interactions")
    .add("awesome_website.component_interaction", ComponentInteraction);
