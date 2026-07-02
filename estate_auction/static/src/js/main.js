import { whenReady } from "@odoo/owl";
import { mountComponent } from "@web/env";
import { AuctionTimer } from "../components/auction_timer/auction_timer";

const config = {
    dev: true
};

whenReady(() => {
    const timerElement = document.getElementById("auction_timer");

    if (!timerElement) {
        return;
    }

    const endTime = timerElement.dataset.endTime;

    mountComponent(AuctionTimer, timerElement, {
        ...config,
        props: {
            endTime
        },
    });
});
