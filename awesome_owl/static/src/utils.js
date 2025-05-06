import { useEffect, useRef } from "@odoo/owl";

export function useAutofocus(refName) {
  let ref = useRef(refName);
  useEffect(
    (el) => el && el.focus(),
    () => [ref.el]
  );
}
