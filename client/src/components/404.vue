<template>
    <h1>Page not found!</h1>
    <el-button type="primary" @click="$router.push('/')">
        Back to homepage
    </el-button>
</template>

<script>
export default {
    'name': 'pageNotFound',
    data() {
        return {

        }
    },
}
</script>