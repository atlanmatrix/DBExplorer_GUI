<template>
    <div id="index-host-card-ctn">
        <h1>Choose one DB server to connect:</h1>
        <el-row :gutter="8">
            <el-col :span="8" v-for="host, idx in hostTableData" :key="'index-host-' + idx">
                <el-card
                        class="box-card"
                        style="cursor: pointer;"
                        shadow="hover"
                        @click="connectDB(host.host)">
                    <div class="text item">
                        <div>{{ host.name || 'unnamed host' }}</div>
                        <!-- <div>{{ host.host }}</div> -->
                    </div>
                </el-card>
            </el-col>
            <el-col :span="8">
                <el-card
                        class="box-card"
                        style="cursor: pointer; border-color: #3f51b5; color: #3f51b5;"
                        shadow="hover"
                        @click="$router.push('/settings')">
                    <div class="text item">
                        <div><span>Edit host configure</span></div>
                    </div>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<style>
    #index-host-card-ctn {
        max-width: 800px;
        margin: 0 auto;
        padding-bottom: 20px;
    }
</style>

<script>
import {vPost} from './utils'

export default {
    'name': 'index',
    data() {
        return {
            hostTableData: [],
        }
    },
    mounted() {
        this.getHostConfig();
    },
    methods: {
        getHostConfig(callback) {
            vPost('/api/cfg/host', {}, (res) => {
                if (res.code === 0) {
                    this.hostTableData = JSON.parse(JSON.stringify(res.data));
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
        connectDB(host) {
            this.$router.push(`/${host}/db/tree`);
        },
    }
}
</script>