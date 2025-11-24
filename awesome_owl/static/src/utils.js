import { useEffect, useRef } from "@odoo/owl";

export function useAutofocus({ refName } = {}) {
    const ref = useRef(refName || "autofocus");

    useEffect((el) => {
        el?.focus();
    }, () => [ref.el]);

    return ref;
}
