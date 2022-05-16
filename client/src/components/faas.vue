<template>
    <div id="markdown-ctn">
        <el-row>
            <el-input
                v-model="name"
                placeholder="Give your function(s) a recognizable name for visiting"
                show-word-limit
                :maxlength="maxFuncNameChars"
            >
                <template #prepend>/func/</template>
            </el-input>
        </el-row>
        <el-row>
            <el-input
                v-model="code"
                type="textarea"
                :rows="10"
                placeholder="Enter your code here, you can enter multiple functions, the first function will be the entry function"
                show-word-limit
                :maxlength="maxFuncCodeChars"
            />
        </el-row>
        <el-row>
            <el-tooltip
                class="box-item"
                effect="dark"
                content="Test your code, make sure you have saved your code first"
                placement="top"
            >
                <el-button
                        type="primary"
                        @click="testFunc"
                        :disabled="status == 'loading'"
                        :loading="status == 'testing'">
                    {{ testBtn[status] }}
                </el-button>
            </el-tooltip>
            <el-tooltip
                class="box-item"
                effect="dark"
                content="Save your code"
                placement="top"
            >
                <el-button
                        type="primary"
                        @click="saveFunc"
                        :disabled="status == 'loading'"
                        :loading="status == 'saving'">
                    {{ saveBtn[status] }}
                </el-button>
            </el-tooltip>
            <el-tooltip
                class="box-item"
                effect="dark"
                content="Take a look at of your Function"
                placement="top"
            >
                <el-button
                    v-show="name">
                    <el-link
                            :href="'/api/faas/' + name"
                            :underline="false"
                            target="_blank"
                            >
                        Preview function
                    </el-link>
                </el-button>
            </el-tooltip>
            <span
                    v-show="cache && enableCache"
                    style="vertical-align: initial;font-size: 12px;color: #999;display: block;position: absolute;right: 0;bottom: 0;"
                    >Cached data: {{ cache }}</span>
        </el-row>
        <el-row>
            <el-input
                v-model="log"
                :rows="8"
                type="textarea"
                disabled
                placeholder="Executing logs will shown here"
            />
        </el-row>
        <el-row>
            <el-input
                v-model="ret"
                :rows="8"
                type="textarea"
                disabled
                placeholder="Return will shown here"
            />
        </el-row>
    </div>
</template>

<style>
    #markdown-ctn {
        max-width: 800px;
        margin: 0 auto;
        padding-bottom: 20px;
    }

    #markdown-ctn blockquote {
        margin: 0;
        padding: 6px 12px;
        border-left: 4px solid #d0d7de;
    }

    #markdown-ctn blockquote p {
        margin: 0;
    }

    #markdown-ctn code,
    #markdown-ctn pre code {
        background-color: #f6f8fa;
        border-radius: 5px;
    }

    #markdown-ctn pre code {
        padding: 18px 15px;
    }

    #markdown-ctn a, #markdown-ctn a:visited {
        color: #0969da;
        text-decoration: none;
    }

    #markdown-ctn a:hover {
        text-decoration: underline;
    }
</style>

<script>
    import {vGet, vPost, vErrorAlert, vSuccessAlert, getFooterRef, pureLocalGetter} from "./utils"
    import 'highlight.js/styles/github.css';

    export default {
        'name': 'FaaS',
        data() {
            return {
                func_id: '',
                log: '',
                ret: '',
                enableCache: false,
                cache: '',
                name: '',
                status: 'loading',
                maxFuncNameChars: 32,
                maxFuncCodeChars: 4096,
                code: 'Loading...',
                testBtn: {
                    'loading': 'Loading...',
                    'testing': 'Testing...',
                    'saving': 'Test',
                    'normal': 'Test',
                },
                saveBtn: {
                    'loading': 'Loading...',
                    'saving': 'Saving...',
                    'testing': 'Save',
                    'normal': 'Save'
                }
            }
        },
        mounted() {
            this.init();
        },
        methods: {
            resetFooterBar(taskName) {
                getFooterRef(this).resetFooterBar(taskName);
            },
            setFooterBar(taskName, status, timeCost, totalTimeCost, errorMsg) {
                getFooterRef(this).setFooterBar(taskName, status, timeCost, totalTimeCost, errorMsg);
            },
            init() {
                let taskName = `Load function ${this.$route.params.func_id}`;
                let status = '';
                let errorMsg = '';

                this.func_id = this.$route.params.func_id;
                this.status = 'loading';

                this.resetFooterBar(taskName);
                let now = Date.now();
                vGet(`/api/faas/${this.func_id}/info`, {}, (res) => {
                    if (res.code == 0) {
                        this.name = res.data.name;
                        this.code = res.data.code;
                        this.cache = res.data.cache;
                        this.enableCache = res.data.enable_cache;
                        status = 'success';
                    } else {
                        vErrorAlert(res.msg);
                        status = 'error';
                    }

                    this.status = 'normal';

                    let interfaceCost = res.cost * 1000;
                    this.setFooterBar(taskName, status, interfaceCost, Date.now() - now, errorMsg);
                }, (error) => {
                    vErrorAlert(error);
                    this.setFooterBar(taskName, 'error', NaN, Date.now() - now, error);
                });
            },
            testFunc() {
                let taskName = `Test function ${this.$route.params.func_id}`;
                let status = '';
                let errorMsg = '';

                let setting = pureLocalGetter('setting');
                let enableCache = setting.enableCache;

                this.func_id = this.$route.params.func_id;
                this.status = 'testing';
                this.resetFooterBar(taskName);
                let now = Date.now();
                vGet(`/api/faas/${this.func_id}`, {
                    is_test: '1',
                    enable_cache: enableCache,
                }, (res) => {
                    if (res.code == 0) {
                        this.log = res.data.log;
                        this.ret = res.data.ret;
                        this.init();
                        vSuccessAlert('Function executed successfully');
                        status = 'success';
                    } else {
                        this.log = '';
                        this.ret = '';
                        vErrorAlert(res.msg);
                        status = 'error';
                    }

                    this.status = 'normal';

                    let interfaceCost = res.cost * 1000;
                    this.setFooterBar(taskName, status, interfaceCost, Date.now() - now, errorMsg);
                }, (error) => {
                    vErrorAlert(error);
                    this.setFooterBar(taskName, 'error', NaN, Date.now() - now, error);
                });
            },
            saveFunc() {
                let taskName = `Save function ${this.$route.params.func_id}`;
                let status = '';
                let errorMsg = '';

                this.resetFooterBar(taskName);
                let now = Date.now();
                this.status = 'saving';

                vPost('/api/faas/create', {
                    "id": this.func_id,
                    "name": this.name,
                    "code": this.code,
                }, (res) => {
                    setTimeout(() => {
                        if (res.code == 0) {
                            vSuccessAlert('Function saved successfully');
                            status = 'success';
                        } else {
                            this.log = '';
                            this.ret = '';
                            vErrorAlert(res.msg);
                            status = 'error';
                        }

                        this.status = 'normal';

                        let interfaceCost = res.cost * 1000;
                        this.setFooterBar(taskName, status, interfaceCost, Date.now() - now, errorMsg);
                    }, 1000);
                }, (error) => {
                    vErrorAlert(error);
                    this.setFooterBar(taskName, 'error', NaN, Date.now() - now, error);
                });
            }
        }
    }
</script>