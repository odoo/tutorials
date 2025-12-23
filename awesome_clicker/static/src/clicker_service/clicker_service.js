import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { reactive } from "@odoo/owl";
import { ClickerModel } from "../clicker_model/clicker_model";
import { browser } from "@web/core/browser/browser";
import { migrate } from "../clicker_migration/clicker_migration";

const clicker_service = {
    dependencies: ["action","effect","notification"],
    start(env, services)
    {

        let model = ClickerModel.fromJSON(browser.localStorage.getItem("clicker_model")) || new ClickerModel()
        model = migrate(model)

        setInterval(() => 
            {
                model.tickBot();
                browser.localStorage.setItem("clicker_model",model.toJSON());

            }, 
        1000*10);
        
        setInterval(() => 
            {
                model.tickFruit();
            }, 
        1000*30);



        document.addEventListener("click",() => model.addClicks(1),true);

        model.event.addEventListener("MILESTONE1K",()=>{
            services.effect.add({type: "rainbow_man",message:"You just leveled up your clicker level"});
        });

        model.event.addEventListener("REWARD",(ev)=>
            {
                const reward = ev.detail;
                let notificationClose = services.notification.add(
                    `Congrats you won : "${reward.description}"`,
                    {
                        type: "success",
                        sticky: true,
                        buttons: [
                            {
                                name : "Collect",
                                onClick: () => 
                                {
                                    reward.apply(model);
                                    notificationClose();
                                    services.action.doAction({
                                        type: "ir.actions.client",
                                        tag: "awesome_clicker.client_action",
                                        target: "new",
                                        name: "Clicker Game"
                                    });
                                },
                                    
                            },
                        ]
                    });
            })

        
        return model;
        
    },
    
};

registry.category("services").add("awesome_clicker.clicker_service",clicker_service)
