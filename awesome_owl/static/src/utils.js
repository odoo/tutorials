import { useEffect, useRef } from "@odoo/owl";

export function useAutoFocus({ refName }) {
    const ref = useRef(refName);
    useEffect((el) => {
        el?.focus();
    }, () => [ref.el])
}
