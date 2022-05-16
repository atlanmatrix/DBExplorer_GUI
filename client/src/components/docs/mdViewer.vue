<template>
  <div id="markdown-ctn">
    <Markdown :source="source" />
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
import {vGet, vErrorAlert, getFooterRef} from '../utils'
import Markdown from 'vue3-markdown-it';
import 'highlight.js/styles/github.css';

export default {
    components: {
        Markdown
    },
    data() {
        return {
            source: '### Loading...'
        }
    },
    mounted() {
        this.fetchMarkdown();
    },
    updated() {
        this.fetchMarkdown();
    },
    methods: {
        resetFooterBar(taskName) {
            getFooterRef(this).resetFooterBar(taskName);
        },
        setFooterBar(taskName, status, timeCost, totalTimeCost, errorMsg) {
            getFooterRef(this).setFooterBar(taskName, status, timeCost, totalTimeCost, errorMsg);
        },
        fetchMarkdown() {
            let taskName = `Load documention: ${this.$route.params.docId}`;
            let status = '';
            let errorMsg = '';

            this.resetFooterBar(taskName);
            let now = Date.now();
            vGet(`/api/doc/md/${this.$route.params.docId}.md`, {}, res => {
                if (res.code == 0) {
                    this.source = res.data;
                    // vSuccessAlert(`${res.msg}s`);
                    status = 'success';
                } else {
                    this.source = res.msg;
                    vErrorAlert(res.msg);
                    status = 'error';
                }

                let interfaceCost = res.cost * 1000;
                this.setFooterBar(taskName, status, interfaceCost, Date.now() - now, errorMsg);
            }, (error) => {
                vErrorAlert(error);
                this.setFooterBar(taskName, 'error', NaN, Date.now() - now, error);
            });
        }
    }
}
</script>