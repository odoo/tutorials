import { whenReady } from "@odoo/owl";
import { mountComponent } from "@web/env";
import { Playground } from "./playground";
import { ToDoList } from "./todolist/todolist";

const config = {
    dev: true,
    name: "Owl Tutorial",
};

whenReady(() => {
    const pathname = window.location.pathname;
    if (pathname === "/awesome_owl") {
        mountComponent(Playground, document.body, config);
    } else if (pathname === "/awesome_owl/todos") {
        mountComponent(ToDoList, document.body, config);
    }
});