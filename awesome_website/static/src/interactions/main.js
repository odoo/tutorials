import { registry } from "@web/core/registry";
import { Interaction } from "@web/public/interaction";

class Main extends Interaction {
    static selector = "main";

    dynamicContent = {
        _root: {
            "t-out": () => (new Date()).toLocaleString(),
        },
    };

}

// registry.category("public.interactions").add("awesome_website.main", Main);
