/** @odoo-module **/

import { Counter } from "../src/counter/counter";
import { click, getFixture, mount } from "@web/../tests/helpers/utils";

let target;

QUnit.module("Components", (hooks) => {
    hooks.beforeEach(async () => {
        target = getFixture();
    });

    QUnit.module("Counter");

    QUnit.debug("Counter is correctly incremented", async (assert) => {
        await mount(Counter, target);
        assert.strictEqual(target.querySelector("body > p").innerHTML, "Counter: 1");
        await click(target, ".btn-primary");
        assert.strictEqual(target.querySelector("body > p").innerHTML, "Counter: 2");
    });
});
