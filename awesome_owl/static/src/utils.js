import { useRef } from "@odoo/owl";
import { onMounted } from "@odoo/owl";

export function useAutoFocus(name) {
    // NOTE; Object remains alive due to (weak)ref stored inside the closure
    // of 'onMounted'.
    let theElement = useRef(name);

    onMounted(() => {
        theElement.el.focus();
        console.log("Executed autofocus");
    });
}