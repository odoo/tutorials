/** @odoo-module **/

import { click, getFixture, patchWithCleanup } from "@web/../tests/helpers/utils";
import { registry } from "@web/core/registry";
import { tooltipService } from "@web/core/tooltip/tooltip_service";
import { uiService } from "@web/core/ui/ui_service";
import { makeView, setupViewRegistries } from "@web/../tests/views/helpers";
import { actionService } from "@web/webclient/actions/action_service";

const serviceRegistry = registry.category("services");

let serverData;
let target;

QUnit.module("Views", (hooks) => {
    hooks.beforeEach(() => {
        serverData = {
            models: {
                order: {
                    fields: {
                        image_url: { string: "Image", type: "char" },
                        description: { string: "Description", type: "char" },
                    },
                    records: [
                        {
                            id: 1,
                            image_url: "",
                            description: "A nice description",
                        },
                        {
                            id: 2,
                            image_url: "",
                            description: "A second nice description",
                        },
                    ],
                },
            },
            views: {},
        };
        setupViewRegistries();
        serviceRegistry.add("tooltip", tooltipService);
        target = getFixture();
        serviceRegistry.add("ui", uiService);
    });

    QUnit.module("GalleryView");

    QUnit.test("open record on image click", async function (assert) {
        assert.expect(3);

        patchWithCleanup(actionService, {
            start() {
                const result = this._super(...arguments);
                return {
                    ...result,
                    switchView(viewType, { resId }) {
                        assert.step(JSON.stringify({ viewType, resId }));
                    },
                };
            },
        });

        await makeView({
            type: "gallery",
            resModel: "order",
            serverData,
            arch: '<gallery image_field="image_url" tooltip_field="description"/>',
        });
        assert.containsOnce(target, ".o_control_panel");
        await click(target, ".row > div:nth-child(1) > div");
        assert.verifySteps([`{"viewType":"form","resId":1}`]);
    });
});
