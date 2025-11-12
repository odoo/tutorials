/** @odoo-module **/

import { useRef, useEffect } from '@odoo/owl';

export function useAutoFocus(name) {
    const elemRef = useRef(name);

    useEffect(() => {
        elemRef.el && elemRef.el.focus()
    }, () => [elemRef.el]);

    return elemRef;
}
