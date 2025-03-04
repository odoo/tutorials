import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";

class AuctionTimer extends Component {
    static template = "estate_auction.auction_timer";
    static props = {
        property : Object
    }
    setup() {
        this.state = useState({
            timeLeft: this.calculateTimeLeft(),
        });

        this.timer = null;

        onWillStart(() => {
            this.startTimer();
        });

        onWillUnmount(() => {
            clearInterval(this.timer);
        });
    }

    calculateTimeLeft() {
        const now = new Date().getTime();
        const end = new Date(this.props.property.auction_end_date).getTime();
        const distance = end - now;

        if (distance <= 0) {
            return "00:00:00";
        }

        const hours = String(Math.floor((distance / (1000 * 60 * 60)) % 24)).padStart(2, "0");
        const minutes = String(Math.floor((distance / (1000 * 60)) % 60)).padStart(2, "0");
        const seconds = String(Math.floor((distance / 1000) % 60)).padStart(2, "0");

        return `${hours}:${minutes}:${seconds}`;
    }

    startTimer() {
        this.timer = setInterval(() => {
            this.state.timeLeft = this.calculateTimeLeft();
            if (this.state.timeLeft === "00:00:00") {
                clearInterval(this.timer);
            }
        }, 1000);
    }


}