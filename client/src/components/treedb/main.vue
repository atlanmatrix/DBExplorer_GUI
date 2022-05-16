<template>
    <div class="view-ctn tree-db-ctn">
        <el-container>
            <el-container style="position: relative;">
                <el-aside width="auto" style="min-width: 320px;">
                    <el-tree
                        :data="treeData"
                        lazy
                        :load="getTreeData2"
                        @node-click="nodeClickHandler"
                        :highlight-current="true"
                        node-key="path">
                        <template #default="{ node, data }">
                            <span class="custom-tree-node">
                                <span>{{ node.label }}</span>
                                <span v-show="data.path.split('\\').length > 2">
                                    <a @click="editKey(node, data)" title="edit node"> <el-icon style="color: #037113;"><edit /></el-icon> </a>&nbsp;
                                    <a @click="addSubkey(node, data)" title="add child node"> <el-icon style="color: #0c58b0;"><circle-plus /></el-icon> </a>&nbsp;
                                    <a @click="deleteKey(node, data)" title="delete node"> <el-icon style="color: #a40707;"><circle-close /></el-icon> </a>&nbsp;
                                    <a @click="generateCode(node, data)" title="code"> <el-icon style="color: #a40707;"><cpu /></el-icon> </a>&nbsp;
                                </span>
                            </span>
                        </template>
                    </el-tree>
                </el-aside>
                <el-main>
                    <el-table :data="tableData" height="100%" style="width: 100%">
                        <el-table-column prop="name" label="Name" width="160" />
                        <el-table-column prop="type" label="Type" width="120" />
                        <el-table-column prop="value" label="Value" width="" />
                        <el-table-column fixed="right" label="Operations" width="240">
                            <template #default="scope">
                                <el-button
                                    @click="editProps(scope.row)"
                                    color="#626aef"
                                    style="color: white;"
                                    size="small"
                                    >Edit</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-main>
            </el-container>
        </el-container>
    </div>
    <el-dialog v-model="editKeyDialogShow" title="Modify key name">
        <el-form :model="form" label-width="96px">
            <el-form-item label="Current:">
                <el-input v-model="oldKeyName" placeholder="" disabled />
            </el-form-item>
            <el-form-item label="New:">
                <el-input v-model="newKeyName" placeholder="Enter new key name" />
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submitEditKey">Update</el-button>
                <el-button @click="editKeyDialogShow = false">Cancel</el-button>
            </el-form-item>
        </el-form>
    </el-dialog>
    <el-dialog v-model="addSubkeyDialogShow" title="Input sub key name">
        <el-form :model="form" label-width="96px">
            <el-form-item label="Key name:">
                <el-input v-model="newSubKeyName" placeholder="" />
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submitAddSubKey">Add</el-button>
                <el-button @click="addSubkeyDialogShow = false">Cancel</el-button>
            </el-form-item>
        </el-form>
    </el-dialog>
    <el-dialog v-model="deleteKeyDialogShow" title="Are your sure to delete?">
        <el-form :model="form" label-width="96px">
            <el-form-item label="Key:">
                <el-input v-model="currNodeData.path" placeholder="" disabled />
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submitDeleteKey">Confirm</el-button>
                <el-button @click="deleteKeyDialogShow = false">Cancel</el-button>
            </el-form-item>
        </el-form>
    </el-dialog>
    <el-dialog v-model="editPropsDialogShow" title="Modify property">
        <el-form :model="form" label-width="96px">
            <el-form-item label="Prop Name:">
                <el-input v-model="propName" placeholder="" disabled />
            </el-form-item>
            <el-form-item label="Old value:">
                <el-input v-model="propOldVal" placeholder="" disabled />
            </el-form-item>
            <el-form-item label="New Value:">
                <el-input v-model="propNewVal" placeholder="Enter new property name" />
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submitEditProps">Update</el-button>
                <el-button @click="editPropsDialogShow = false">Cancel</el-button>
            </el-form-item>
        </el-form>
    </el-dialog>
    <!-- Search box -->
    <el-dialog v-model="searchDialogShow" title="Search everything">
        <el-input
                ref="searchBoxRef"
                v-model="searchText"
                @keyup.enter="globalSearch"
                placeholder="Input keywords"
                >
        </el-input>
        <el-tabs v-model="activeName" class="demo-tabs">
            <el-tab-pane label="Device" name="device">
                <el-table
                        :data="deviceSearchResult"
                        height="320px"
                        style="width: 100%;"
                        border
                        @expand-change="handleDeviceExpandChange(row, expandedRows)"
                        >
                    <el-table-column type="expand">
                        <template #default="props">
                            <p>ID: {{ props.row.id }}</p>
                            <p>Device Name: {{ props.row.label }}</p>
                            <p>IP: {{ props.row.ip }}</p>
                            <p>Device Type: {{ props.row.device_type }}</p>
                        </template>
                    </el-table-column>
                    <el-table-column prop="id" label="ID" width="" />
                    <el-table-column prop="label" label="Device Name" width="" />
                    <el-table-column prop="ip" label="IP" width="" />
                    <el-table-column prop="device_type" label="Device Type" width="" />
                </el-table>
            </el-tab-pane>
            <el-tab-pane label="Group" name="group">
                <el-table :data="groupSearchResult" height="320px" style="width: 100%;" border>
                    <el-table-column prop="id" label="ID" width="" />
                    <el-table-column prop="label" label="Group Name" width="" />
                    <el-table-column prop="path" label="Path" width="" />
                </el-table>
            </el-tab-pane>
            <el-tab-pane label="Monitor Template" name="plugindata">
                <el-table :data="pluginSearchResult" height="320px" style="width: 100%;" border>
                    <el-table-column prop="id" label="ID" width="" />
                    <el-table-column prop="path" label="Path" width="" />
                </el-table>
            </el-tab-pane>
        </el-tabs>
        <el-row justify="end">
            <el-button type="primary" @click="$router.push('/settings')" size="small">advanced</el-button>
            <el-button type="default" @click="searchDialogShow = false" size="small">close</el-button>
        </el-row>
    </el-dialog>
    <el-drawer
        v-model="autoCodeDrawerShow"
        title="Auto Code"
        direction="rtl"
        size="60%"
    >
        <Markdown :source="source" />
    </el-drawer>
</template>
<script>
    import {vPost, vSuccessAlert, vErrorAlert, getFooterRef} from "../utils"
    import Markdown from 'vue3-markdown-it';
    import 'highlight.js/styles/github.css';

    export default {
        components: {
            Markdown
        },
        'name': 'dbMain',
        data() {
            return {
                editKeyDialogShow: false,
                oldKeyName: '',
                newKeyName: '',
                newSubKeyName: '',
                addSubkeyDialogShow: false,
                deleteKeyDialogShow: false,
                editPropsDialogShow: false,
                propName: '',
                propOldVal: '',
                propNewVal: '',
                searchText: '',
                host: '',
                fullPath: '',
                treeData: [{
                    label: '',
                },],
                tableData: [],
                currNode: {},
                autoCodeDrawerShow: false,
                source: '# Loading...',
                footerRef: null,
                searchDialogShow: false,
                activeName: 'device',
                deviceSearchResult: [],
                groupSearchResult: [],
                pluginSearchResult: [],
                searchLoading: false,
                hostTableData: [
                    {'name': 'demo.jiankongyi.com', 'host': 'demo.jiankongyi.com', 'isStar': true},
                ],
                tmpHostTableData: [
                    {'name': 'demo.jiankongyi.com', 'host': 'demo.jiankongyi.com', 'isStar': true},
                ],
            }
        },
        mounted() {
            this.init();
            this.getTreeData();

            let _this = this;
            document.onkeydown = function (e) {
                let metaKey = e.metaKey;
                let ctrlKey = e.ctrlKey;
                if (metaKey && e.keyCode == 75) {
                    _this.searchDialogShow = true;
                    console.info('cmd+k')
                    _this.$nextTick(() => {
                        _this.$refs.searchBoxRef.focus()
                    })
                } else if (ctrlKey && e.keyCode == 75) {
                    e.preventDefault();
                    _this.searchDialogShow = true;
                    console.info('ctrl+k')
                    _this.$nextTick(() => {
                        _this.$refs.searchBoxRef.focus()
                    })
                    console.info(_this.$parent.$refs)
                }
            }
        },
        watch: {
            '$route.path': function (to, from) {
                console.info(to, '->', from);
                this.init();
                this.getTreeData();
            }
        },
        methods: {
            init() {
                this.host = this.$route.params.ip;
                this.getHostConfig();
                // let siteDBData = this.$utils.localGetter(this.host)
                // this.fullPath = (siteDBData && siteDBData['fullPath']) || ''
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
            resetFooterBar(taskName) {
                getFooterRef(this).resetFooterBar(taskName);
            },
            setFooterBar(taskName, status, timeCost, totalTimeCost, errorMsg) {
                getFooterRef(this).setFooterBar(taskName, status, timeCost, totalTimeCost, errorMsg);
            },
            setFooterBarDBHost(host) {
                getFooterRef(this).setHost(host);
            },
            nodeClickHandler(data, node) {
                this.currNode = node;
                this.currNodeData = data;
                this.currNode.loaded = false;
                this.currNode.expand();
            },
            editProps(row) {
                let taskName = `Waiting for edit property`;
                this.propName = row.name;
                this.propOldVal = row.value;
                this.propNewVal = row.value;
                this.editPropsDialogShow = true;
                this.setFooterBar(taskName, 'warn', NaN, NaN, '');
            },
            submitEditProps () {
                let taskName = `Edit property for ${this.currNodeData.path}`;
                let status = '';
                let errorMsg = '';

                this.resetFooterBar(taskName);
                let now = Date.now();
                vPost('/api/db/tree/props/update', {
                    host: this.host,
                    path: this.currNodeData.path,
                    prop_name: this.propName,
                    prop_val: this.propNewVal,
                }, (res) => {
                    if (res.code === 0) {
                        this.tableData = res.data;
                        this.editPropsDialogShow = false;
                        vSuccessAlert(`Edit property successfully!`);
                        status = 'success';
                    } else {
                        vErrorAlert(res.msg);
                        status = 'error';
                    }

                    let interfaceCost = res.cost * 1000;
                    this.setFooterBar(taskName, status, interfaceCost, Date.now() - now, errorMsg);
                }, (error) => {
                    vErrorAlert(error);
                    this.setFooterBar(taskName, 'error', NaN, Date.now() - now, error);
                });
            },
            editKey (node, data) {
                let taskName = `Waiting for edit key name`;
                this.node = node;
                this.currNodeData = data;
                this.oldKeyName = this.currNodeData.label;
                this.newKeyName = this.currNodeData.label;
                this.editKeyDialogShow = true;
                this.setFooterBar(taskName, 'warn', NaN, NaN, '');
            },
            submitEditKey () {
                let taskName = `Replace key name ${this.currNodeData.path} to ${this.newKeyName}`;
                let status = '';
                let errorMsg = '';

                this.resetFooterBar(taskName);
                let now = Date.now();
                vPost('/api/db/tree/update', {
                    host: this.host,
                    path: this.currNodeData.path,
                    sub_key: this.newKeyName,
                }, (res) => {
                    if (res.code === 0) {
                        this.editKeyDialogShow = false;
                        this.node.parent.loaded = false;
                        this.node.parent.expand();
                        vSuccessAlert(`Edit key successfully!`);
                        status = 'success';
                    } else {
                        vErrorAlert(res.msg);
                        status = 'error';
                    }

                    let interfaceCost = res.cost * 1000;
                    this.setFooterBar(taskName, status, interfaceCost, Date.now() - now, errorMsg);
                }, (error) => {
                    vErrorAlert(error);
                    this.setFooterBar(taskName, 'error', NaN, Date.now() - now, error);
                });
            },
            addSubkey (node, data) {
                let taskName = `Waiting for add new key`;
                this.node = node;
                this.currNodeData = data;
                this.addSubkeyDialogShow = true;
                this.setFooterBar(taskName, 'warn', NaN, NaN, '');
            },
            submitAddSubKey() {
                let taskName = `Add new key ${this.newSubKeyName} under ${this.currNodeData.path}`;
                let status = '';
                let errorMsg = '';

                this.resetFooterBar(taskName);
                let now = Date.now();
                vPost('/api/db/tree/add', {
                    host: this.host,
                    path: this.currNodeData.path,
                    sub_key: this.newSubKeyName,
                }, (res) => {
                    if (res.code == 0) {
                        this.addSubkeyDialogShow = false;
                        this.node.loaded = false;
                        this.node.expand();
                        vSuccessAlert(`Add sub key successfully!`);
                        status = 'success';
                    } else {
                        vErrorAlert(res.msg);
                        status = 'error';
                        errorMsg = res.msg;
                    }

                    let interfaceCost = res.cost * 1000;
                    this.setFooterBar(taskName, status, interfaceCost, Date.now() - now, errorMsg);
                }, (error) => {
                    vErrorAlert(error);
                    this.setFooterBar(taskName, 'error', NaN, Date.now() - now, error);
                });
            },
            deleteKey (node, data) {
                let taskName = `Waiting for delete key confirm: ${this.currNodeData.path}`;
                this.node = node;
                this.currNodeData = data;
                this.deleteKeyDialogShow = true;
                this.setFooterBar(taskName, 'warn', NaN, NaN, '');
            },
            submitDeleteKey() {
                let taskName = `Delete key: ${this.currNodeData.path}`;
                let status = '';
                let errorMsg = '';

                this.resetFooterBar(taskName);
                let now = Date.now();
                vPost('/api/db/tree/delete', {
                    host: this.host,
                    path: this.currNodeData.path,
                }, (res) => {
                    if (res.code === 0) {
                        this.deleteKeyDialogShow = false;
                        this.node.parent.loaded = false;
                        this.node.parent.expand();
                        vSuccessAlert('Delete key successfully');
                        status = 'success';
                    } else {
                        vErrorAlert(res.msg);
                        status = 'error';
                    }

                    let interfaceCost = res.cost * 1000;
                    this.setFooterBar(taskName, status, interfaceCost, Date.now() - now, errorMsg);
                }, (error) => {
                    vErrorAlert(error);
                    this.setFooterBar(taskName, 'error', NaN, Date.now() - now, error);
                });
            },
            getTreeData() {
                let taskName = `Connect to DB ${this.host}`;
                let status = '';
                let errorMsg = '';

                let form = new FormData();
                form.append("host", this.host);
                form.append("path", this.path);

                this.resetFooterBar(taskName);
                let now = Date.now();
                vPost(`/api/db/tree`, form, (res) => {
                    if (res.code == 0) {
                        let data = res.data;
                        this.treeData = data.sub_keys;
                        this.tableData = data.props;
                        status = 'success';
                    } else {
                        vErrorAlert(res.msg);
                        status = 'error';
                        errorMsg = res.msg;
                    }

                    let interfaceCost = res.cost * 1000;
                    this.setFooterBar(taskName, status, interfaceCost, Date.now() - now, errorMsg);
                    this.setFooterBarDBHost(this.host);
                }, (error) => {
                    vErrorAlert(error);
                    this.setFooterBar(taskName, 'error', NaN, Date.now() - now, error);
                });
            },
            getTreeData2(node, resolve) {
                let taskName = '';
                let status = '';
                let errorMsg = '';

                if (!this.host) {
                    return
                }
                let form = new FormData();
                form.append("host", this.host);

                if (node) {
                    let pathList = [node.data.label]
                    let parent = node.parent
                    while (parent) {
                        if (parent.data.label) {
                            pathList.splice(0, 0, parent.data.label)
                            parent = parent.parent
                        } else {
                            break
                        }
                    }

                    let fullpath = pathList.join("\\")
                    let file = pathList.shift();
                    form.append("filename", file);
                    form.append("path", pathList.join("\\"));
                    taskName = `Query ${fullpath}`;

                    let now = Date.now();
                    this.resetFooterBar(taskName);
                    vPost(`/api/db/tree`, form, (res) => {
                        if (res.code == 0) {
                            let data = res.data;
                            resolve(data.sub_keys);
                            this.tableData = data.props;
                            this[fullpath] = data.props;
                            this.$utils.localSetter(this.host, [fullpath], this);
                            status = 'success';
                        } else {
                            vErrorAlert(res.msg);
                            status = 'error';
                            errorMsg = res.msg;
                        }

                        let interfaceCost = res.cost * 1000;
                        this.setFooterBar(taskName, status, interfaceCost, Date.now() - now, errorMsg);
                    }, (error) => {
                        vErrorAlert(error);
                        resolve([]);
                        this.setFooterBar(taskName, 'error', NaN, Date.now() - now, error);
                    });
                }
            },
            generateCode(node, data) {
                let taskName = 'Auto generate code';
                let status = '';
                let errorMsg = '';

                this.currNodeData = data;
                this.autoCodeDrawerShow = true;

                this.resetFooterBar(taskName);
                let now = Date.now();
                vPost(`/api/db/tree/auto_code`, {
                    host: this.host,
                    path: this.currNodeData.path,
                }, (res) => {
                    if (res.code === 0) {
                        this.source = res.data;
                        status = 'success';
                    } else {
                        status = 'error';
                        vErrorAlert(res.msg);
                    }

                    let interfaceCost = res.cost * 1000;
                    this.setFooterBar(taskName, status, interfaceCost, Date.now() - now, errorMsg);
                }, (error) => {
                    vErrorAlert(error);
                    this.setFooterBar(taskName, 'error', NaN, Date.now() - now, error);
                });
            },
            globalSearch(row) {
                console.info(row);
                let taskName = `Search text: ${this.searchText}`;
                let status = '';
                let errorMsg = '';

                this.resetFooterBar(taskName);
                this.searchLoading = true;
                let now = Date.now();
                vPost('/api/db/tree/search', {
                    host: this.host,
                    search_text: this.searchText,
                }, (res) => {
                    if (res.code === 0) {
                        this.deviceSearchResult = res.data['device'];
                        this.pluginSearchResult = res.data['plugin'];
                        this.groupSearchResult = res.data['group'];
                        // this.deleteKeyDialogShow = false;
                        // this.node.parent.loaded = false;
                        // this.node.parent.expand();
                        // vSuccessAlert('Delete key successfully');
                        status = 'success';
                    } else {
                        vErrorAlert(res.msg);
                        status = 'error';
                    }

                    let interfaceCost = res.cost * 1000;
                    this.setFooterBar(taskName, status, interfaceCost, Date.now() - now, errorMsg);
                    this.searchLoading = false;
                }, (error) => {
                    vErrorAlert(error);
                    this.setFooterBar(taskName, 'error', NaN, Date.now() - now, error);
                    this.searchLoading = false;
                });
            },
            handleDeviceExpandChange(row, expandedRows) {
                console.info(row, expandedRows);
            }
        }
    }
</script>
<style>
    html, body, #app, .el-main, .el-container, .el-aside, .tree-db-ctn, .explorer-ctn {
        height: 100%;
    }
    .tree-db-ctn {
        height: calc(100% - 84px);
    }

    .tree-db-ctn .el-tree {
        padding: 10px 20px;
    }

    .el-main {
        padding: 10px 20px;
        height: calc(100% - 74px);
    }

    .custom-tree-node {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 14px;
        padding-right: 8px;
    }

    .custom-tree-node .el-icon {
        opacity: 0;
    }

    .custom-tree-node:hover .el-icon {
        opacity: 1;
    }

    .el-aside .el-input.el-input--default {
        padding: 0 20px;
    }

    .host-menu-item {
        height: 32px;
        line-height: 32px;
    }

    #host-menu-ctn {
        height: 100%;
    }

    #host-menu-ctn li.el-menu-item {
        display: block;
        max-width: 180px;
        overflow-x: hidden;
        text-overflow: ellipsis;
    }
    .el-tabs__nav-wrap::after {
        height: 0;
    }
</style>
