import { whenReady } from "@odoo/owl";
import { mountComponent } from "@web/env";

import { Playground } from "./playground";
import { Counter } from "./counter";

const config = {
  dev: true,
  name: "Owl Tutorial",
};

whenReady(() => {
  const page = document.body.dataset.page;

  if (page === "counter") {
    mountComponent(Counter, document.body, config);
  } else {
    mountComponent(Playground, document.body, config);
  }
});
