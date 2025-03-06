import { registry } from "@web/core/registry";
import { useState, onMounted } from "@odoo/owl";
import { Component } from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class CountdowmTimer extends Component{
    static template = "estate_auction.CountdownTimerWidget";
    static props = {
        ...standardFieldProps,
    };

    
    setup(){
        this.state = useState({timeLeft : this.calculateTimeLeft()});

        onMounted(() =>{registry
            this.startCountdown();
        });
    }

    calculateTimeLeft(){
        const endDate = new Date(this.props.endDate);
        const now = new Date();
        const diff = endDate - now;

        if(diff <= 0){
            return {
                days: 0, hours: 0, minutes: 0, seconds: 0
            };
        }

        return {
            days: Math.floor(diff / (1000 * 60 * 60 * 24)),
            hours: Math.floor((diff / (1000 * 60 * 60)) % 24),
            minutes: Math.floor((diff / (1000 * 60)) % 60),
            seconds : Math.floor((diff / 1000) % 60)
        };
    }

    startCountdown(){
        this.interval = setInterval(() => {
            this.state.timeLeft = this.calculateTimeLeft();

        }, 1000);
    }

    get timerText(){
        const { days, hours, minutes, seconds } = this.state.timeLeft;
        return '${days}d ${hours}h ${minutes}m ${seconds}s';
    }

    willUnmount(){
        clearInterval(this.interval);
    }

}

export const countdowmTimer = {
    component: CountdowmTimer,
}

registry.category("fields").add("countdown_timer", countdowmTimer);

