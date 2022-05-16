import { createWebHistory, createRouter } from "vue-router";

import pageNotFound from "./components/404";
import index from "./components/index";
import dbMain from "./components/treedb/main"
import mdViewer from "./components/docs/mdViewer"
import comingSoon from "./components/comingSoon"
import FaaS from "./components/faas"
import FaaSList from "./components/faas/list"
import setting from "./components/setting"

const routes = [
    { path: "/", name: "index", component: index, meta: { title: 'Welcome to DB Explorer' },},
    { path: "/coming_soon", name: "comingSoon", component: comingSoon, meta: { title: 'Coming Soon...' },},
    { path: "/doc/:docId", name: "mdViewer", component: mdViewer, meta: { title: 'Document' },},
    { path: "/db/tree", name: "dbMain", component: dbMain, meta: { title: 'TreeDB Explorer' },},
    { path: "/:ip/db/tree", name: "dbMain", component: dbMain, meta: { title: 'TreeDB Explorer' },},
    { path: "/faas/list", name: "FaaSList", component: FaaSList, meta: { title: 'FaaS List' },},
    { path: "/faas/:func_id/edit", name: "FaasEdit", component: FaaS, meta: { title: 'Edit FaaS' },},
    { path: "/settings", name: "settings", component: setting, meta: { title: 'System Preferences' },},
    { path: "/:catchAll(.*)", name: "pageNotFound", component: pageNotFound, meta: { title: 'Ooooops..Page not found!' },},
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    document.title = to.meta.title;
    next();
})

export default router;
