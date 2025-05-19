import { EventBus } from '@odoo/owl';
import { Reactive } from '@web/core/utils/reactive';
import { humanNumber } from '@web/core/utils/numbers';
import { browser } from '@web/core/browser/browser';
import { findMigrationPath, getValidNum } from './utils';

class Resource {
    constructor(name, clickCost, level, icon, count, description) {
        this.name = name;
        this.clickCost = clickCost;
        this.level = level;
        this.icon = icon;
        this.count = count;
        this.description = description;
    }

    buy(clicker) {
        if (
            clicker.level < this.level ||
            clicker.clicks < this.clickCost
        ) {
            return false;
        }
        clicker.increment(-this.clickCost);
        this.count++;
        return true;
    }
};

class Tree extends Resource {
    constructor(name, clickCost, fruit, fruitIcon) {
        super(name, clickCost, 4, 'fa fa-tree', 0, `1 ${fruit} / 30 seconds`);
        this.fruit = {
            name: fruit,
            count: 0,
            icon: fruitIcon
        };
    }
};

export class ClickerModel extends Reactive {
    static version = 2;
    static migrations = [
        {
            fromVersion: 1,
            toVersion: 2,
            apply: state => {
                state.version = 2;
                state.plantResources.length = 3;
                state.plantResources[2] = {
                    trees: 0,
                    fruits: 0
                }
            }
        },
        {
            fromVersion: 2,
            toVersion: 1,
            apply: state => {
                state.version = 1;
                state.plantResources.length = 2;
            }
        }
    ];
    constructor() {
        super();
        this.bus = new EventBus();
        this.clicks = 0;
        this.humanClicks = '0';
        this.level = 0;
        this.milestones = [
            {
                event: 'MILESTONE_1k',
                clicks: 1000,
                level: 1,
                description: "Milestone reached! You can now buy clickbots"
            },
            {
                event: 'MILESTONE_5k',
                clicks: 5000,
                level: 2,
                description: "Milestone reached! You can now buy bigbots"
            },
            {
                event: 'MILESTONE_100k',
                clicks: 100000,
                level: 3,
                description: "Milestone reached! You can now buy power"
            },
            {
                event: 'MILESTONE_1M',
                clicks: 1000000,
                level: 4,
                description: "Milestone reached! Yo can now buy trees"
            }
        ];

        this.clickBot = new Resource('ClickBot', 1000, 1, 'fa fa-android', 0, '10 clicks/10 seconds');
        this.bigBot = new Resource('BigBot', 5000, 2, 'fa fa-android', 0, '100 clicks / 10 seconds');
        this.power = new Resource('Power', 50000, 3, 'fa fa-bolt', 1, 'power multiplier');
        this.trees = [
            new Tree('Pear Tree', 1000000, 'Pear', 'fa fa-apple'),
            new Tree('Cherry Tree', 1000000, 'Cherry', 'fa fa-apple'),
            new Tree('Peach Tree', 1500000, 'Peach', 'fa fa-apple')
        ];

        this.clickResources = [
            {
                name: 'Bots',
                icon: 'fa fa-android',
                resources: [this.clickBot, this.bigBot],
            },
            {
                name: 'Power multiplier',
                icon: 'fa fa-bolt',
                resources: [this.power],
            },
        ];

        this.resources = [
            ...this.clickResources,
            {
                name: 'Trees',
                icon: 'fa fa-tree',
                resources: this.trees
            }
        ];

        this.loadState();

        setInterval(() => {
            const inc = this.power.count * (
                10 * this.clickBot.count +
                100 * this.bigBot.count
            );
            this.increment(inc);
            this.saveState();
        }, 10000);

        setInterval(() => {
            for (const tree of this.trees) {
                tree.fruit.count += tree.count;
            }
        }, 30000);
    }

    saveState() {
        const state = {
            version: ClickerModel.version,
            clicks: this.clicks,
            level: this.level,
            clickResources: [],
            plantResources: []
        };
        for (const resourceType of this.clickResources) {
            for (const resource of resourceType.resources) {
                state.clickResources.push(resource.count);
            }
        }
        for (const tree of this.trees) {
            state.plantResources.push({
                trees: tree.count,
                fruits: tree.fruit.count
            });
        }
        browser.localStorage.setItem('clicker_game', JSON.stringify(state));
    }

    loadState() {
        const stateJSON = browser.localStorage.getItem('clicker_game');
        if (!stateJSON) {
            return;
        }
        const state = JSON.parse(stateJSON);
        if (state.version != ClickerModel.version) {
            console.log("Pre-Migration State: ", JSON.stringify(state));
            const migrationPath = findMigrationPath(ClickerModel.migrations, state.version, ClickerModel.version);
            if (!migrationPath) {
                console.log("no migration path found");
            } else {
                console.log("migration path:", migrationPath);
                for (const migration of migrationPath) {
                    migration.apply(state);
                }
            }
            console.log("Post-Migration State: ", JSON.stringify(state));
        }

        this.clicks = getValidNum(state.clicks, this.clicks);
        this.humanClicks = humanNumber(this.clicks);
        this.level = getValidNum(state.level, this.level);

        if (state.clickResources) {
            let i = 0;
            for (const resourceType of this.clickResources) {
                for (const resource of resourceType.resources) {
                    if (i >= state.clickResources.length) {
                        break;
                    }
                    resource.count = getValidNum(state.clickResources[i], resource.count);
                    i++;
                }
                if (i >= state.clickResources.length) {
                    break;
                }
            }
        }

        if (state.plantResources) {
            for (let i = 0; i < state.plantResources.length; i++) {
                if (i >= this.trees.length) {
                    break;
                }
                this.trees[i].count = getValidNum(state.plantResources[i].trees, this.trees[i].count);
                this.trees[i].fruit.count = getValidNum(state.plantResources[i].fruits, this.trees[i].fruit.count);
            }
        }
    }

    increment(inc) {
        this.clicks += inc;
        this.humanClicks = humanNumber(this.clicks);

        for (const milestone of this.milestones) {
            if (
                this.level < milestone.level &&
                this.clicks >= milestone.clicks
            ) {
                this.bus.trigger(milestone.event);
                this.level = milestone.level;
            }
        }
    }

    getResourceTypeCount(resourceType) {
        let count = 0;
        for (const resource of resourceType.resources) {
            count += resource.count;
        }
        return count;
    }
};
