<template>
    <div id="footer-wrp">
        <span style="position: absolute; left: 0; height: 24px; line-height: 24px;">
            <span>Host: </span>
            <span :class="{
                        'success_status': taskStatus == 'success',
                        'warn_status': taskStatus == 'warn',
                        'error_status': taskStatus == 'error',
                    }"
                    style="cursor: pointer;"
                    @click="switchHost">
                {{ host }}
            </span>
        </span>
        <span>
            <span>Task: </span>
            <span :class="{
                        'success_status': taskStatus == 'success',
                        'warn_status': taskStatus == 'warn',
                        'error_status': taskStatus == 'error',
                    }">
                {{ taskName }}
            </span>
        </span>
        <span>
            <span>Status: </span>
            <span :class="{
                        'success_status': taskStatus == 'success',
                        'warn_status': taskStatus == 'warn',
                        'error_status': taskStatus == 'error',
                    }">
                {{ taskStatus }}
            </span>
        </span>
        <span v-show="errorMsg">
            <span>Msg: </span>
            <span class="error_status">
                {{ errorMsg }}
            </span>
        </span>
        <span id="footer-btn-sys-info-tc" v-show="!isNaN(timeCost)">
            <span>Interface Cost: </span>
            <span :class="{
                        'low_latency': timeCost < 300,
                        'middle_latency': timeCost > 300 && timeCost < 900,
                        'high_latency': timeCost > 900,
                    }">
                {{ (timeCost &lt; 1) ? '&lt;1' : parseInt(timeCost) }}ms
            </span>
        </span>
        <span id="footer-btn-sys-info-ttc" v-show="!isNaN(totalTimeCost)">
            <span>RTT: </span>
            <span :class="{
                        'low_latency': totalTimeCost < 300,
                        'middle_latency': totalTimeCost > 300 && totalTimeCost < 900,
                        'high_latency': totalTimeCost > 900,
                    }">
                {{ (totalTimeCost &lt; 1) ? '&lt;1' : parseInt(totalTimeCost) }}ms
            </span>
        </span>
    </div>
</template>

<style>
    #footer-wrp {
        position: fixed;
        left: 0;
        right: 0;
        bottom: 0;
        height: 24px;
        border-top: 1px solid #e6e6e6;
        border-image: linear-gradient(to right, #8f41e9,#f23e3e, #578aef) 1;
        background-color: #fff;
        text-align: right;
        z-index: 9999;
    }

    #footer-wrp > span {
        padding: 0 6px;
        font-size: 12px;
        color: #999;
    }

    #footer-wrp span.low_latency,
    #footer-wrp span.success_status {
        color: green;
    }

    #footer-wrp span.middle_latency,
    #footer-wrp span.warn_status {
        color: orange;
    }

    #footer-wrp span.high_latency,
    #footer-wrp span.error_status {
        color: #f44;
    }

    #footer-wrp .el-select-v2__wrapper {
        border: none;
    }
</style>

<script>
export default {
    'name': 'vFooter',
    data() {
        return {
            host: '',
            timeCost: NaN,
            totalTimeCost: NaN,
            taskName: 'None',
            taskStatus: '',
            errorMsg: '',
            options: [{
                value: '192.168.8.40',
                label: '192.168.8.40'
            }],
        }
    },
    methods: {
        setHost(host) {
            this.host = host;
        },
        setFooterBar(taskName, status, timeCost, totalTimeCost, errorMsg) {
            this.taskName = taskName;
            this.taskStatus = status;
            this.timeCost = timeCost;
            this.totalTimeCost = totalTimeCost;
            this.errorMsg = errorMsg;
        },
        resetFooterBar(taskName) {
            this.taskName = taskName;
            this.taskStatus = 'loading...';
            this.timeCost = NaN;
            this.totalTimeCost = NaN;
            this.errorMsg = '';
        },
        switchHost () {
            this.$router.push('/settings');
        }
    },
}
</script>