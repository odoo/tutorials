
import { browser } from "@web/core/browser/browser";
import { onMounted, onWillUnmount } from "@odoo/owl";
export function useInterval(callback , duration)
{
    let interval;
    onMounted(() => (interval = browser.setInterval(callback, duration)));
    onWillUnmount(() => (browser.clearInterval(interval)));
}
