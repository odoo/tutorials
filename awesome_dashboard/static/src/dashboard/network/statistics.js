/** @odoo-module */

import {registry} from "@web/core/registry";
import {reactive} from "@odoo/owl";

const myService = {
    dependencies: ["rpc"],
    start(env, {rpc}) {
        this.fnc=null;
        const exec = ()=>{this.fnc();}
        const stats = reactive({ isReady: false },exec)
        async function myfnc() {
            let temp= await rpc("/awesome_dashboard/statistics");
            Object.assign(stats, temp, { isReady: true });
        }
        setInterval(myfnc, 1000);
        myfnc();
        return {stats:stats,pexec:(fnc)=>{this.fnc=fnc}};
    }

};


registry.category("services").add("awesome_dashboard.statistics", myService);