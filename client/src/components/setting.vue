<template>
    <div id="setting-ctn" class="view-ctn pref-tab-ctn">
        <section>
            <el-row justify="space-between">
                <span style="color: #3f51b5;">Host name and IP/Domain configure</span>
                <el-button
                        color="#3f51b5"
                        style="border-color: #3f51b5;"
                        plain
                        size="small"
                        @click="addNewHostConfig">
                    + Add host
                </el-button>
            </el-row>
            <div class="item-section">
                <el-collapse
                        :accordion="true"
                        v-model="activeCollapse">
                    <el-collapse-item
                            :title="'' + item.name + ''"
                            :name="'host-' + idx"
                            :key="'host-' + idx"
                            v-for="(item, idx) in tmpHostTableData"
                            >
                        <template #title>
                            <el-icon style="color: green;"><monitor /></el-icon>&nbsp;
                            {{ item.name }}
                        </template>
                        <div style="margin-top: 3px;">
                            <span style="display: inline-block; width: 200px;">Name:</span>
                            <el-input v-model="item.name" size="small" @blur="saveHostConfig"></el-input>
                        </div>
                        <div style="margin-top: 3px;">
                            <span style="display: inline-block; width: 200px">IP/Domain:</span>
                            <el-input v-model="item.host" size="small" @blur="saveHostConfig"></el-input>
                        </div>
                        <div style="margin-top: 3px;">
                            <span style="display: inline-block; width: 200px">Loaded DB files:</span>
                            <el-tag
                                    style=""
                                    :class="{
                                        'db-file-tag': true,
                                        'editable-db-file-tag': dbFile.editable
                                    }"
                                    v-for="dbFile, dbFileIdx in item.dbFiles"
                                    effect="plain"
                                    :type="dbFile.editable ? 'warning': 'info'"
                                    :key="dbFile.name"
                                    :closable="dbFile.editable"
                                    @click="updateDbFile(dbFile)"
                                    @close="deleteDbFile(idx, dbFileIdx)"
                                    >
                                {{ dbFile.name }}
                            </el-tag>
                            <div style="padding-left: 200px;">
                                <el-button
                                        color="#3f51b5"
                                        style="border-color: #3f51b5;"
                                        size="small"
                                        plain
                                        @click="addDBFile(idx)">
                                    + Add File
                                </el-button>
                            </div>
                        </div>
                        <div style="margin-top: 3px; text-align: right;">
                            <el-button
                                    type="danger"
                                    plain
                                    size="small"
                                    @click="deleteHostConfig(idx)">
                                <el-icon><delete /></el-icon>
                                &nbsp; Delete config
                            </el-button>
                        </div>
                    </el-collapse-item>
                </el-collapse>
            </div>
        </section>
        <section>
            <el-row justify="space-between">
                <span style="color: #3f51b5;">DB search rules</span>
            </el-row>
            <div class="item-section">
                <el-table id="setting-search-rules-table" :data="defaultSearchRules" style="width: 100%">
                    <el-table-column prop="name" label="Name">
                        <template #default="scope">
                            <span>{{ scope.row.name }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="searchPath" label="Search Path">
                        <template #default="scope">
                            <span>{{ scope.row.searchPath }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="fields" label="Search Fields">
                        <template #default="scope">
                            <p>{{ JSON.stringify(scope.row.fields) }}</p>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
        </section>
        <section>
            <el-row justify="space-between">
                <span style="color: #3f51b5;">FaaS Cache</span>
            </el-row>
            <div class="item-section">
                <el-checkbox v-model="setting.enableCache" label="Enable Cache" size="large" text-color="#3fb1b5"/>
                <div style="margin-bottom: 8px;">
                   <span style="font-size: 12px; color: #999;">*With FaaS cache enabled, your latest test result will be stored and returned while others access your Function.</span>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
import {vSuccessAlert, getHeaderRef, getFooterRef, pureLocalGetter, vPost, vConfirm} from "./utils"
import {searchRule} from "./settings"

export default {
    'name': 'setting',
    data() {
        return {
            isAddStatus: false,
            activeCollapse: 'host-0',
            newHostConfig: {
                dbFiles: [],
            },
            activeIndex: '/setting/host',
            faasEnableCache: false,
            editHostTableDataShow: false,
            saveLoading: false,
            hostTableData: [],
            tmpHostTableData: [],
            setting: {},
            defaultSearchRules: searchRule,
            editDBFileDialogShow: false,
            oldDbFileName: '',
            currDbFileObj: '',
        }
    },
    mounted() {
        this.getHostConfig();

        vPost('/api/cfg/default_host_config', {}, (res) => {
            if (res.code === 0) {
                this.newHostConfig = res.data;
            } else {
                console.error(res.msg)
            }
        });

        let setting = pureLocalGetter('setting');
        this.setting = setting;

        this.activeIndex = this.$route.path;
        let taskName = `Load ${this.$route.path.slice(1).split("/").join(' -> ')}`;
        taskName = 'Load settings';
        this.setFooterBar(taskName, 'success', NaN, NaN, '');
    },
    watch: {
        '$route.path': function (to, from) {
            let taskName = `Load ${to.slice(1).split("/").join(' -> ')}`;
            console.info(to, from);
            this.activeIndex = to;
            this.setFooterBar(taskName, 'success', NaN, NaN, '');
        },
        'setting': {
            deep: true,
            handler: function () {
                localStorage.setItem('setting', JSON.stringify(this.setting || {}));
            }
        }
    },
    methods: {
        resetFooterBar(taskName) {
            getFooterRef(this).resetFooterBar(taskName);
        },
        setFooterBar(taskName, status, timeCost, totalTimeCost, errorMsg) {
            getFooterRef(this).setFooterBar(taskName, status, timeCost, totalTimeCost, errorMsg);
        },
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
        addNewHostConfig() {
            this.tmpHostTableData.push(JSON.parse(JSON.stringify(this.newHostConfig)));
            this.saveConfig('host', this.tmpHostTableData, () => {
                this.getHostConfig(() => {
                    this.activeCollapse = `host-${this.hostTableData.length - 1}`;
                });
            });
        },
        addDBFile(idx) {
            this.tmpHostTableData[idx].dbFiles.push({
                name: 'temp',
                editable: true
            });
            this.saveHostConfig();
        },
        updateDbFile(dbFile) {
            this.oldDbFileName = dbFile.name;
            this.currDbFileObj = dbFile;
            this.editDBFileDialogShow = true;
        },
        confirmUpdateDbFile() {
            this.saveHostConfig(() => {
                this.editDBFileDialogShow = false;
            });
        },
        deleteDbFile(idx, dbFileIdx) {
            vConfirm('Are you sure to remove this DB file?', '', () => {
                this.tmpHostTableData[idx].dbFiles.splice(dbFileIdx, 1);
                this.saveHostConfig();
            });
        },
        saveHostConfig(callback) {
            this.saveConfig('host', this.tmpHostTableData, () => {
                this.getHostConfig(callback);
            });
        },
        saveConfig(configName, configData, callback) {
            vPost(`/api/cfg/${configName}`, {
                op: 'update',
                data: configData
            }, (res) => {
                if (res.code === 0) {
                    callback && callback();
                } else {
                    vSuccessAlert(res.msg);
                }
            })
        },
        addNewHostConfigViaKeyboard(idx) {
            if (idx == this.tmpHostTableData.length - 1) {
                this.addNewHostConfig();
            }
        },
        setHostAsDefault (idx) {
            for (let item of this.tmpHostTableData) {
                item.isStar = false;
            }
            this.tmpHostTableData[idx].isStar = true;
        },
        deleteHostConfig (idx) {
            vConfirm('Are you sure to delete this host?', '', () => {
                this.tmpHostTableData.splice(idx, 1);
                this.saveConfig('host', this.tmpHostTableData, () => {
                    this.getHostConfig();
                });
            });
        },
        confirmTmpHostTableData() {
            let taskName = `Saving host configuration`;

            this.resetFooterBar(taskName);
            this.saveLoading = true;
            setTimeout(() => {
                getHeaderRef(this).hostTableData = this.hostTableData;
                this.saveLoading = false;
                this.setFooterBar(taskName, 'success', NaN, NaN, '');
                vSuccessAlert('Settings saved!');
            }, 600);
        },
        cancelTmpHostTableData() {
            this.tmpHostTableData = JSON.parse(JSON.stringify(this.hostTableData));
        },
    },
}
</script>
<style>
    #setting-ctn li.el-menu-item {
        display: block;
        font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
  'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
        font-size: 14px !important;
        height: 36px;
        line-height: 36px;
        text-align: right;
        padding-bottom: 40px;
    }

    #setting-ctn .el-input {
        width: 320px;
    }

    .pref-tab-ctn {
        padding: 20px 20px 45px;
        max-width: 800px;
        margin: 0 auto;
    }

    .item-section {
        border-radius: 8px;
        border: 1px solid #ebebeb;
        /* box-shadow: inset 1px 1px 3px #babecc, inset -3px -3px 6px white; */
        padding: 0 12px;
    }

    .item-section .el-collapse {
        border: none;
    }

    .db-file-tag {
        margin-right: 6px;
        margin-bottom: 6px;
        cursor: default;
    }

    .editable-db-file-tag {
        cursor: pointer;
    }

    .el-checkbox__input.is-checked+.el-checkbox__label {
        color: orange;
    }
    .el-checkbox__input.is-checked .el-checkbox__inner {
        color: orange;
        background-color: orange;
        border-color: orange;
    }
</style>