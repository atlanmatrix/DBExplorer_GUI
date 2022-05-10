let searchRule = [{
    name: 'Device',
    searchPath: 'ccubase\\{CCUList}\\1\\1.SD',
    fields: {
        '{key}': 'ID',
        'mxlabel': 'Device Name',
        '_target_ip': 'IP',
        'mxdevicetype': 'Device Type'
    }
}, {
    name: 'Group',
    searchPath: 'ccubase\\{CCUList}\\1\\1.SG',
    fields: {
        '{key}': 'ID',
        'mxlabel': 'Group Name',
        '{path}': 'Path'
    }
}, {
    name: 'Monitor Template',
    searchPath: 'base\\PluginData',
    fields: {
        '{key}': 'Monitor Name',
        '{path}': 'Path'
    }
}];

export {
    searchRule
}
