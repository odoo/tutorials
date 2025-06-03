import { whenReady } from "@odoo/owl";
import { mountComponent } from "@web/env";
import { Playground } from "./playground";
import { TodoList } from "./components/todolist/todolist";

const config = {
    dev: true,
    name: "Owl Tutorial",
};

whenReady(() =>
    mountComponent(
        window.location.pathname === "/awesome_owl/todos"
            ? TodoList
            : Playground,
        document.body,
        config
    )
);
