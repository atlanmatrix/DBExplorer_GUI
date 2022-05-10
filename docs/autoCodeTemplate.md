# Auto generate code(Python)
### Get sub key list under current key
```python
def get_sub_key_lst():
    try:
        from jkyweb.module.public.TreeModel import TreeModel
    except Exception:
        from jkyweb.module.TreeModel import TreeModel

    db = TreeModel()

    host = '$$HOST$$'
    main_key = '$$MAIN_KEY$$'
    sub_key = r'$$SUB_KEY$$'
    filename = '$$FILENAME$$'

    sub_keys = db.open(main_key, sub_key, host, filename).sub_keys()
    return sub_keys
```

### Get items' map or list of current key
```python
def get_item_map():
    """
    Return:
        {
            <prop_name1>: <prop_value1>, 
            <prop_name2>: <prop_value2>, 
            ...
        }
    """
    try:
        from jkyweb.module.public.TreeModel import TreeModel
    except Exception:
        from jkyweb.module.TreeModel import TreeModel

    db = TreeModel()

    host = '$$HOST$$'
    main_key = '$$MAIN_KEY$$'
    sub_key = r'$$SUB_KEY$$'
    filename = '$$FILENAME$$'

    items = db.open(main_key, sub_key, host, filename).items()
    return items


def get_item_lst():
    """
    Return:
        [
            {'name': <prop_name1>, 'value': <prop_value1>}, 
            {'name': <prop_name2>, 'value': <prop_value2>}, 
            ...
        ]
    """
    try:
        from jkyweb.module.public.TreeModel import TreeModel
    except Exception:
        from jkyweb.module.TreeModel import TreeModel

    db = TreeModel()

    host = '$$HOST$$'
    main_key = '$$MAIN_KEY$$'
    sub_key = r'$$SUB_KEY$$'
    filename = '$$FILENAME$$'

    items = db.open(main_key, sub_key, host, filename).items()

    return [{
        'name': key,
        'value': val
    } for key, val in items.items()]
```

### Get sub keys and sub keys' items
```python
def get_key_items_map():
    """
    Return:
        {
            <prop_name1>: <prop_value1>, 
            <prop_name2>: <prop_value2>, 
            ...
        }
    """
    try:
        from jkyweb.module.public.TreeModel import TreeModel
    except Exception:
        from jkyweb.module.TreeModel import TreeModel

    host = '$$HOST$$'
    main_key = '$$MAIN_KEY$$'
    sub_key = r'$$SUB_KEY$$'
    filename = '$$FILENAME$$'

    key_items = db.open(main_key, sub_key, host, filename).sub_items()
    return key_items
```
