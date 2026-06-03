import { registry } from "@web/core/registry";
import { Interaction } from "@web/public/interaction";

class Main extends Interaction {
  static selector = "main";

  dynamicContent = {
    _root: {
      "t-out": () => {
        const now = new Date();
        return now.toLocaleString('en-US');
      }
    }
  };
}

// registry.category("public.interactions").add("awesome_website.main", Main);
