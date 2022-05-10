import { createApp } from 'vue'
import Markdown from 'vue3-markdown-it';
import ElementPlus from 'element-plus'
import * as ElementIcons from '@element-plus/icons-vue'
import 'element-plus/dist/index.css'
import App from './App.vue'
import axios from 'axios'
import router from './router'
import { createStore } from 'vuex'
import * as Utils from './components/utils'
import * as settings from './components/settings'


const store = createStore({
    state () {
        return {
            isLogin: false,
            user: {},
            role: 0
        }
    },
    mutations: {
        login(state, user) {
            state.isLogin = true;
            state.role = user.role || 0;
            state.user = user;
        },
        logout(state) {
            state.isLogin = false;
            state.role = 0;
            state.user = {};
        }
    }
});

axios.defaults.withCredentials = true;

let app = createApp(App);
app.use(ElementPlus)
app.use(router)
app.use(store)
app.use(Markdown)
for (let icon in ElementIcons) {
    app.component(icon, ElementIcons[icon])
}

app.config.globalProperties.$utils = Utils;
app.config.globalProperties.$settings = settings;

app.component()
app.mount('#app')
