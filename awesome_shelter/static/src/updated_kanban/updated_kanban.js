import { registry } from "@web/core/registry";
import {  kanbanView } from "@web/views/kanban/kanban_view";
import { useInterval } from "../utlis/utils";




class UpdatedKanban extends kanbanView.Controller
{
    setup()
    {
        super.setup();
        useInterval(this.reload.bind(this),10000);
    }
    reload()
    {
        console.log("reloaded");
        this.model.load();
    }

}
const updatedKanban = 
{
    ...kanbanView,
    Controller: UpdatedKanban,

};

registry.category("views").add("updated_kanban",updatedKanban);
