import axios from 'axios'
import { ElNotification, ElMessageBox } from 'element-plus'


const vGet = (url, params, callback, errorCallback) => {
    axios.get(url, {
        params: params
    }).then(response => {
        let data = response.data;
        callback(data);
    }).catch(error => {
        if (errorCallback) {
            errorCallback(error);
        } else {
            vErrorAlert(error);
        }
    });
};

const vPost = (url, params, callback, errorCallback) => {
    axios.post(url, params).then(response => {
        let data = response.data;
        callback(data);
    }).catch(error => {
        if (errorCallback) {
            errorCallback(error);
        } else {
            vErrorAlert(error);
        }
    });
};

const vRedirect = (that, redirect='', login='/user/login/phone') => {
    vGet('/api/user/status/', {}, (data) => {
        if (!data.login_status) {
            that.$router.push(`${login}?redirect=${redirect}`);
        }
    });
};

const vManagemanetRedirect = (that, redirect='', login='/manage/login') => {
    vGet('/api/user/status/', {}, (data) => {
        if (!data.login_status) {
            that.$router.push(`${login}?redirect=${redirect}`);
        }
    });
};

const vSuccessAlert = (msg, title='') => {
    vAlert('success', msg, title);
};

const vErrorAlert = (msg, title='') => {
    vAlert('error', msg, title);
};

const vInfoAlert = (msg, title='') => {
    vAlert('info', msg, title);
};

const vAlert = (type, msg, title='') => {
    ElNotification({
        title: title,
        message: msg,
        type: type
    });
};

const vConfirm = (msg, type='Warning', callback) => {
    ElMessageBox.confirm(
        msg || 'Are you sure?',
        type || 'Warning',
        {
            confirmButtonText: 'OK',
            cancelButtonText: 'Cancel',
            type: 'warning',
        }).then(callback).catch(() => {
            console.info('cancelled');
        })
}

const localSetter = (name, fields, vueApp) => {
    let storedData = {}

    if (name in localStorage) {
        storedData = localStorage[name];
        storedData = JSON.parse(storedData);
    }

    for (let field of fields) {
        if (field in vueApp) {
            storedData[field] = vueApp[field];
        }
    }

    localStorage[name] = JSON.stringify(storedData);
};

const pureLocalGetter = (name) => {
    if (!(name in localStorage)) return {};

    let storedData = localStorage[name];
    storedData = JSON.parse(storedData);

    return storedData;
};

const localGetter = (name, fields, vueApp) => {
    if (!(name in localStorage)) return;

    let storedData = localStorage[name];
    storedData = JSON.parse(storedData);

    if (vueApp) {
        for (let field of fields) {
            if (field in storedData) {
                vueApp[field] = storedData[field];
            }
        }
    } else {
        return storedData
    }
}

let footer = {
    'sysInfo': ''
};

const getMainAppRefs = (comp) => {
    while (!('footer' in comp.$refs)) {
        comp = comp.$parent;
    }

    return comp.$refs
};

const getHeaderRef = (comp) => {
    while (!('header' in comp.$refs)) {
        comp = comp.$parent;
    }

    return comp.$refs.header
};

const getFooterRef = (comp) => {
    while (!('footer' in comp.$refs)) {
        comp = comp.$parent;
    }

    return comp.$refs.footer
};

export {
    vGet, vPost, vRedirect,
    vSuccessAlert, vErrorAlert, vInfoAlert, vAlert,
    vConfirm,
    vManagemanetRedirect,
    pureLocalGetter,
    localGetter, localSetter,
    footer,
    getMainAppRefs, getHeaderRef, getFooterRef
}
