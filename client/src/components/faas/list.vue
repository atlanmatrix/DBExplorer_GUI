<template>
    <div id="faas-list-markdown-ctn">
        <el-row v-if="source" justify="space-between">
            <h3>Function list:</h3>
            <el-button
                    type="primary"
                    style="margin: 1em 0;"
                    @click="$router.push('/faas/create')"
                    >
                {{ source ? 'Create' : ', create one!' }}
            </el-button>
        </el-row>
        <el-row v-else>
            <h3>No function found,
                <el-button type="primary" @click="$router.push('/faas/create')">
                    Create now!
                </el-button>
            </h3>
        </el-row>
        <Markdown :source="source" />
    </div>
</template>

<style>
    #faas-list-markdown-ctn {
        max-width: 800px;
        margin: 0 auto;
        padding-bottom: 20px;
    }

    #faas-list-markdown-ctn blockquote {
        margin: 0;
        padding: 6px 12px;
        border-left: 4px solid #d0d7de;
    }

    #faas-list-markdown-ctn blockquote p {
        margin: 0;
    }

    #faas-list-markdown-ctn code,
    #faas-list-markdown-ctn pre code {
        background-color: #f6f8fa;
        border-radius: 5px;
    }

    #faas-list-markdown-ctn pre code {
        padding: 18px 15px;
    }

    #faas-list-markdown-ctn a, #faas-list-markdown-ctn a:visited {
        color: #0969da;
        text-decoration: none;
    }

    #faas-list-markdown-ctn a:hover {
        text-decoration: underline;
    }
</style>

<script>
    import {vGet, vErrorAlert, getFooterRef} from "../utils"
    import Markdown from 'vue3-markdown-it';
    import 'highlight.js/styles/github.css';

    export default {
        components: {
            Markdown
        },
        'name': 'FaaSList',
        data() {
            return {
                source: '### Loading...'
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
                let taskName = `Get function list`;
                let status = '';
                let errorMsg = '';

                this.resetFooterBar(taskName);
                let now = Date.now();
                vGet(`/api/faas/list`, {}, (res) => {
                    if (res.code == 0) {
                        this.source = res.data;
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
        }
    }
</script>