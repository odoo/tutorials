export class DashboardItemManager {
    constructor(id, item, loc, grid) {
        this.id = id
        this.item = item
        this.loc = loc
        this.grid = grid
    }

    remove() {
        this.grid.removeItem(this)
    }

    move(loc) {
        this.grid.moveItem(this, loc)
    }
}

export class DashboardGridManager {
    items = []
    idAcc = 1;

    grid = []
    gridRows = 0
    gridColumns = 4

    extendRows(to) {
        for (; this.gridRows <= to; this.gridRows++)
            this.grid.push(Array(this.gridColumns))
    }

    isOccupied(loc, except = []) {
        if (
            loc.pos.x < 0 || loc.pos.y < 0 ||
            loc.size.x < 1 || loc.size.y < 1 ||
            loc.pos.x >= this.gridColumns || loc.pos.x + loc.size.x > this.gridColumns
        )
            throw new RangeError();

        this.extendRows(loc.pos.y + loc.size.y - 1)

        return this.grid.slice(loc.pos.y, loc.pos.y + loc.size.y)
            .some((a) =>
                a.slice(loc.pos.x, loc.pos.x + loc.size.x).some((a) => a && !except.includes(a))
            )
    }

    get(id) {
        if (id <= 0 || id >= this.idAcc)
            return undefined;
        return this.items[id - 1]
    }

    addItem(item, loc) {
        if (this.isOccupied(loc))
            throw new Error("Loc already taken !")

        const gridItem = new DashboardItemManager(this.idAcc++, item, loc, this);
        this.items.push(gridItem)

        this._addLocOnGrid(loc, gridItem.id)

        return gridItem
    }

    moveItem(item, loc) {
        if (this.isOccupied(loc, [item.id]))
            throw new Error("Loc already taken !")

        this._removeLocOnGrid(item.loc)

        item.loc = loc
        this._addLocOnGrid(item.loc, item.id)
    }

    removeItem(item) {
        this._removeLocOnGrid(item.loc)
        item.loc = undefined
        item.id = undefined
        item.grid = undefined
        this.items[id - 1] = undefined;
    }

    _addLocOnGrid(loc, id) {
        for (let x = loc.pos.x; x < loc.pos.x + loc.size.x; x++)
            for (let y = loc.pos.y; y < loc.pos.y + loc.size.y; y++)
                this.grid[y][x] = id
    }

    _removeLocOnGrid(loc) {
        for (let x = loc.pos.x; x < loc.pos.x + loc.size.x; x++)
            for (let y = loc.pos.y; y < loc.pos.y + loc.size.y; y++)
                this.grid[y][x] = undefined
    }
}