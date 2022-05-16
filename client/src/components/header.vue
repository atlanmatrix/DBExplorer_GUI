<template>
    <el-affix :offset="0" style="">
        <el-menu
            mode="horizontal"
            background-color="white"
            text-color="#545c64"
            active-text-color="#4083dc"
            :default-active="$route.path"
            router
            :activeIndex="activeIndex"
            index="1"
        >
            <el-menu-item index="/" style="height: 58px;">
                <span style="font-weight: 600; font-size: 16px;">「 DB Explorer 」</span>
            </el-menu-item>
            <el-sub-menu style="" index="/host">
                <template #title="">
                    <el-icon style="color: green;">
                        <monitor />
                    </el-icon>
                    Hosts
                </template>
                <el-menu-item
                        :index="'/' + item.host + '/db/tree'"
                        v-for="item in hostTableData"
                        :key="item.host"
                        :title="item.host"
                        >
                    <el-icon style="color: orange;">
                        <star-filled v-if="item.isStar"/>
                        <star style="color: #aaa;" v-else/>
                    </el-icon>
                    {{ item['name'] }}
                </el-menu-item>
                <el-menu-item index="/add_host" style="border-top: 1px solid #ccc;">
                    <el-icon style="color: #0c58b0;">
                        <edit />
                    </el-icon>
                    Edit host config
                </el-menu-item>
            </el-sub-menu>
            <el-menu-item index="/faas/list">
                <el-icon style="color: #9c0cb0;">
                    <lightning />
                </el-icon>
                FaaS
            </el-menu-item>
            <!--el-menu-item index="/doc/ChangeLog">
                <el-icon style="color: #b0460c;">
                    <clock />
                </el-icon>
                Change Log
            </el-menu-item-->
            <el-menu-item index="/settings" style="position: absolute; right: 0;">
                <el-icon style="color: #4083dc;">
                    <setting />
                </el-icon>
                Preferences
            </el-menu-item>

            <el-menu-item index="/doc/list">
                <el-icon style="color: #0c58b0;">
                    <document />
                </el-icon>
                Docs
            </el-menu-item>
        </el-menu>
    </el-affix>
</template>

<script>
import {vGet, vPost} from './utils'

export default {
    'name': 'vHeader',
    data() {
        return {
            activeIndex: '/demo.jiankongyi.com/db/tree',
            hostTableData: [
                {'name': 'demo.jiankongyi.com', 'host': 'demo.jiankongyi.com'},
            ],
            tmpHostTableData: [
                {'name': 'demo.jiankongyi.com', 'host': 'demo.jiankongyi.com'},
            ],
        }
    },
    mounted() {
        this.getHostConfig();
    },
    watch: {
        '$route.path': function (to, from) {
            console.info(to, from)
            if (to == '/add_host') {
                this.$router.push('/settings');
            } else if (to == '/faas/create') {
                vGet('/api/faas/create', {}, (res) => {
                    if (res.code == 0) {
                        this.$router.push(`/faas/${res.data}/edit`)
                    } else {
                        console.error()
                    }
                })
            }
        }
    },
    methods: {
        getHostConfig(callback) {
            vPost('/api/cfg/host', {}, (res) => {
                if (res.code === 0) {
                    this.hostTableData = JSON.parse(JSON.stringify(res.data));
                    this.tmpHostTableData = JSON.parse(JSON.stringify(res.data));
                    try{
                        callback && callback();
                    } catch {
                        console.warn('Invalid callback');
                    }
                } else {
                    console.error(res.msg)
                }
            });
        },
    }
}
</script>
<style>
    li.el-menu-item {
        font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
  'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
        font-size: 14px !important;
    }

    .input-ctn * {
        vertical-align: middle;
    }
</style>