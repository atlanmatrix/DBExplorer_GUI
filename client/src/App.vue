<template>
    <v-header ref="header"></v-header>
    <router-view/>
    <v-footer ref="footer"></v-footer>
</template>

<script>
import vHeader from "./components/header"
import vFooter from "./components/footer"

export default {
    name: 'App',
    data() {
        return {
            msg: 'hello'
        }
    },
    methods: {

    },
    components: {
        'v-header': vHeader,
        'v-footer': vFooter
    }
}
</script>

<style>
html, body {
    margin: 0;
    padding: 0;
}

#app {
    font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
  'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #2c3e50;
}

.el-row {
    margin: 20px 0;
}

.el-col {
    margin-bottom: 20px;
}

.view-ctn {
    margin-bottom: 25px;
}
</style>
