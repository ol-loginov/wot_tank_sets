window.EditableTankSetsStatus = (window.EditableTankSetsStatus || []);

function info(arg) {
    window.EditableTankSetsStatus.push(arg);
    console.info(arg);
}

info('import libs');
import {ModelObserver} from "../libs/model.js";
import {pxToRem, remToPx} from "../libs/common.js";
import {showTooltip, hideTooltip} from "../libs/views.js";

if ('EditableTankSetsView' in window) {
    info(`panic! panic!`);
    throw new Error(`нельзя съесть шоколадку два раза...`)
}

const view = {
    /** @type {HTMLDivElement} */
    list: null,
    /** @type {HTMLDivElement} */
    title: null,

    model: null,
    modelCheckpoint: null,

    listDisplay: null,
    titleDisplay: null
};
window.EditableTankSetsView = view;

function addHeightRem(el, add) {
    if (!el)return;

    const style = getComputedStyle(el);
    if (!style || !('height' in style)) {
        return;
    }

    let height = null;

    const remTest = /(.+)rem$/.exec(style.height);
    if (remTest) {
        height = parseFloat(remTest [1]);
    }

    const pxTest = /(.+)px$/.exec(style.height);
    if (pxTest) {
        height = pxToRem(parseFloat(pxTest [1]));
    }

    if (!height) return;

    el.style.height = `${Math.max(20, height + add)}rem`;
}

function cleanupUI() {
    if (view.title)         view.title.remove();
    if (view.list)         view.list.remove();

    view.title = view.titleDisplay = null;
    view.list = view.listDisplay = null;
}

function disposeFilterUI() {
    if (view.title && !document.body.contains(view.title)) {
        view.title = null;
    }
    if (view.list && !document.body.contains(view.list)) {
        view.list = null;
    }
}

class LiveElement {
    constructor(selector) {
        this.element = null;
        this.selector = selector;
    }

    get() {
        if (this.element != null && !document.body.contains(this.element)) {
            this.element = null;
        }
        if (this.element == null) {
            this.element = this.selector();
        }
        return this.element;
    }
}

class Lazy {
    constructor(factory) {
        this.value = null;
        this.factory = factory;
    }

    get(param) {
        if (this.value == null)
            this.value = this.factory(param);
        return this.value;
    }
}

const filterPopoverBodyRef = new LiveElement(() => document.querySelector('div.FilterPopover_body_9e82b944'));
const filterSectionsRef = new LiveElement(() => {
    const popoverBody = filterPopoverBodyRef.get();
    if (!popoverBody) return null;
    return popoverBody.querySelector('div.VerticalScroll_content_62cb6120')
});

function restoreFilterUI() {
    disposeFilterUI();

    if (!view.model) return;

    const model = view.model;
    if (!model.modEnabled) {
        cleanupUI();
        return;
    }

    const popoverBody = filterPopoverBodyRef.get();
    if (!popoverBody) {
        // info('no popover body found');
        return false;
    }
    const filterSections = filterSectionsRef.get();
    if (!filterSections) {
        // info('no popover filter sections found');
        return false;
    }

    var created = false;

    view.title = view.title || popoverBody.querySelector('#editableTankSetsTitle');
    if (!view.title) {
        info('create editableTankSetsTitle');
        view.title = dom('div', {id: 'editableTankSetsTitle', className: 'FormatText_db904f12 FilterPopover_category_aa274a28'});
        view.titleDisplay = null;
        filterSections.appendChild(view.title);

        addHeightRem(popoverBody.querySelector('div.FilterPopover_scroll_bce24275'), 50);
        created = true;
    }

    view.list = view.list || popoverBody.querySelector('#editableTankSetsList');
    if (!view.list) {
        info('create editableTankSetsList');
        view.list = dom('div', {id: 'editableTankSetsList', className: 'FilterPopover_toggleContainer_c7079ba8 FilterPopover_toggleContainer__type_38a25c90'});
        view.listDisplay = null;
        filterSections.appendChild(view.list);
        created = true;
    }

    if (created) {
        updateFilterUI();
    }

    return true;
}

const ActiveButtonClass = 'Toggle_cdf77db0 Toggle_base__theme-primary_3e3de333 Toggle_base__activated_d584e080 FilterPopover_toggle_747f4b53 FilterPopover_toggle__activated_19a04a6d';
const InactiveButtonClass = 'Toggle_cdf77db0 Toggle_base__theme-primary_3e3de333 FilterPopover_toggle_747f4b53';

const HiddenCardClass = 'EditableTankSet--hide';

function updateFilterUI() {
    if (!view.model) return;

    const model = view.model;
    if (!model.modEnabled) {
        cleanupUI();
        return;
    }

    if (view.title && view.titleDisplay != model.groupTitle) {
        view.titleDisplay = model.groupTitle;

        view.title.textContent = model.groupTitle;
    }

    if (view.list && view.listDisplay != model.collections) {
        view.listDisplay = model.collections;

        while (view.list.firstChild)
            view.list.removeChild(view.list.firstChild);

        /**
         <div class="Toggle_cdf77db0 Toggle_base__theme-primary_3e3de333 FilterPopover_toggle_747f4b53" data-name="Toggle">
         <div class="Toggle_border_3d0d0d39"></div>
         <div class="Toggle_background_78cd67c0"></div>
         <div class="Toggle_bulb_fe6d0fba"></div>
         <div class="Toggle_overlay_e2999686"></div>
         <div class="Toggle_content_17eff4d2">
         <div class="FilterPopover_specialsIcons_5a3d8e7" style="background-image: url(img://uri.png); background-repeat: no-repeat no-repeat; background-size: contain; background-position-x: 50.000000%; background-position-y: 50.000000%; " src="img://gui/maps/icons/hangar/filter/special/bonus.png"></div>
         </div>
         </div>

         icon path: img://gui/maps/icons/../maps/icons/mod_editable_tank_sets/1.png
         image path: img://gui/maps/icons/hangar/filter/special/bonus.png
         */

        const collections = JSON.parse(model.collections);
        collections.forEach(collection => {
            const n = collection.n;
            const title = collection.title || "";

            const words = title.trim()
                .split(/[\s-]+/)
                .filter(e=>e.length > 0)
                .map(e=>e.charAt(0).toUpperCase());
            let abbr;
            if (words.length > 1) {
                abbr = words[0] + words[words.length - 1];
            } else if (words.length > 0) {
                abbr = words[0];
            } else {
                abbr = `${n}`;
            }

            const button =
                dom('div', {dataCollection: n, className: collection.active ? ActiveButtonClass : InactiveButtonClass},
                    dom('div', {className: 'Toggle_border_3d0d0d39'}),
                    dom('div', {className: 'Toggle_background_78cd67c0'}),
                    dom('div', {className: 'Toggle_bulb_fe6d0fba'}),
                    dom('div', {className: 'Toggle_overlay_e2999686'}),
                    dom('div', {className: 'Toggle_content_17eff4d2'},
                        dom('div', {className: 'VehicleLevel_3c938122 FilterPopover_vehicleLevel_41885117', text: abbr})
                    ),
                );
            button.onclick = function () {
                toggleCollection(n);
            };
            button.onmouseenter = function () {
                showTooltip(collection.title);
            };
            button.onmouseleave = function () {
                hideTooltip();
            };
            view.list.appendChild(button);
        });
    }
}

function toggleCollection(n) {
    console.info(`toggle collection ${n}`);

    const model = view.model;
    if (!model) return;

    const collections = JSON.parse(model.collections);
    for (const c of collections) {
        if (c.n === n) {
            c.active = !c.active;
            console.info(`collection.${n}.active=${c.active}`)
        }
    }

    const actives = collections
        .filter(e => e.active)
        .map(e => e.n);

    model.collections = JSON.stringify(collections);
    model.onSave({"actives": JSON.stringify(actives)});
}

function dom(tagName, opts, ...children) {
    const element = document.createElement(tagName);
    Object.keys(opts).forEach(k => {
        const v = opts[k];
        if (k === 'text') {
            element.textContent = v;
        } else element[k] = v;
    });

    if (children) {
        children.forEach(child => element.appendChild(child));
    }
    return element;
}

const carouselContentLive = new LiveElement(() => {
    const pageCarousel = document.querySelector('.Page_carousel_2e3eb473');
    if (!pageCarousel)return null;

    return pageCarousel.querySelector('.CarouselSkeleton_content_b18f8dd7');
});

const carouselCards = new Map();

function findCarousel() {
    const carouselContent = carouselContentLive.get();
    if (!carouselContent) return;

    const fiberPropRef = new Lazy((node) => {
        const prop = Object.keys(node).filter(n => n.startsWith('__reactFiber$'))[0];
        return typeof prop === "string" ? prop : null;
    });

    for (const lastInvID of carouselCards.keys()) {
        const lastCard = carouselCards.get(lastInvID);
        if (!document.body.contains(lastCard)) {
            carouselCards.delete(lastInvID);
        }
    }

    const currentVehicles = new Set();

    for (const vehicleCard of carouselContent.querySelectorAll('.vehicle-card')) {
        const details = vehicleCard.querySelector('.Information_details_e5340a0c');
        if (!details) continue;

        const fiber = details[fiberPropRef.get(details)];
        if (fiber && fiber.return && fiber.return.memoizedProps && fiber.return.memoizedProps.vehicle && fiber.return.memoizedProps.vehicle.inventoryId) {
            const invID = fiber.return.memoizedProps.vehicle.inventoryId;
            currentVehicles.add(invID);

            const lastCard = carouselCards.get(invID);
            if (lastCard && lastCard === vehicleCard) {
                continue;
            }
            carouselCards.set(invID, vehicleCard);
        }
    }

    for (const lastInvID of carouselCards.keys()) {
        if (!currentVehicles.has(lastInvID)) {
            carouselCards.delete(lastInvID);
        }
    }

    console.info(`collect ${currentVehicles.size} cards. [${Array.from(currentVehicles).join(', ')}]`)
}

function updateCarousel() {
    if (!view.model) return;

    const model = view.model;
    if (!model.modEnabled) {
        cleanupUI();
        return;
    }

    console.info(`current selected tanks: ${model.visibleSet}`)
    let visibleSet = JSON.parse(model.visibleSet);
    if (visibleSet != null) visibleSet = new Set(visibleSet);

    for (const invID of carouselCards.keys()) {
        const element = carouselCards.get(invID);
        if (visibleSet == null || visibleSet.has(invID)) {
            showCard(element);
        } else {
            hideCard(element);
        }
    }
}

function showCard(/** @type {HTMLDivElement} */ element) {
    if (!element.classList.contains(HiddenCardClass)) return;
    element.classList.remove(HiddenCardClass);
}

function hideCard(/** @type {HTMLDivElement} */ element) {
    if (element.classList.contains(HiddenCardClass)) return;
    element.classList.add(HiddenCardClass);
}

function main() {
    view.ModelObserver = ModelObserver;

    // Create model observer
    const modelObserver = ModelObserver("VehicleFilterModel");

    // Initialize UI logic once the engine is fully ready
    info('engine.whenReady');
    engine.whenReady.then(() => {
        // Keep button in sync with model changes (alerts count etc.)
        modelObserver.onUpdate(m => {
            const model = m.EditableTankSets;
            if (view.model == null || model.checkpoint != view.modelCheckpoint) {
                view.model = model;
                view.modelCheckpoint = model.checkpoint;
                restoreFilterUI();
            }
        });
        modelObserver.subscribe();

        restoreFilterUI();
    });

    const observer = new MutationObserver(() => {
        const start = new Date().getTime();
        restoreFilterUI();
        const finish = new Date().getTime();
        console.info(`dom changes observed in ${(finish - start) / 1000.0} sec`);
    });

    observer.observe(document.body, {childList: true, subtree: true});
}

try {
    info('start main');
    main();
} catch (e) {
    info('error');
    info(e)
}
