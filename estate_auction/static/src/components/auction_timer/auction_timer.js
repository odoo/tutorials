import { Component, useState, onMounted, onWillUnmount } from "@odoo/owl";

export class AuctionTimer extends Component {
    static template = "estate_auction.AuctionTimer";

    static props = {
        endTime: String
    };

    setup() {
        this.state = useState({
            remaining: "00:00:00:00",
            isExpired: false
        });

        const utcString = this.props.endTime.replace(" ", "T") + "Z";
        this.endTime = new Date(utcString);

        onMounted(() => {
            this.updateTimer();

            this.interval = setInterval(() => {
                this.updateTimer();
            }, 1000);
        });

        onWillUnmount(() => {
            clearInterval(this.interval);
        });
    }

    updateTimer() {
        const remaining = this.getRemainingTime();

        this.state.remaining = remaining;

        if (remaining === "00:00:00:00") {
            this.state.isExpired = true;
        }
    }

    getRemainingTime() {
        const now = new Date();
        const difference = this.endTime - now;
        
        if (difference <= 0) {
            clearInterval(this.interval);
            return "00:00:00:00";
        }

        const days = String(
            Math.floor(difference / (1000 * 60 * 60 * 24))
        ).padStart(2, "0");

        const hours = String(
            Math.floor(
                (difference % (1000 * 60 * 60 * 24)) /
                (1000 * 60 * 60)
            )
        ).padStart(2, "0");

        const minutes = String(
            Math.floor(
                (difference % (1000 * 60 * 60)) /
                (1000 * 60)
            )
        ).padStart(2, "0");

        const seconds = String(
            Math.floor(
                (difference % (1000 * 60)) /
                1000
            )
        ).padStart(2, "0");

        return `${days}:${hours}:${minutes}:${seconds}`;
    }
}
