# -*- coding: utf-8 -*-


def get_nested_value(key_path: list, dict_data: dict):
    """
    获取字典类型数据深层key值
    :param key_path: key所处路径 -- 请求参数示例：["result", "message"]
    :param dict_data: 字典数据  -- 请求参数示例：{"result": {"code": 404, "message": "页面地址不存在"}}
    :return: value值[未找到相应数据返回None]  -- 响应数据示例：页面地址不存在
    """
    if isinstance(dict_data, dict):
        for k, v in dict_data.items():
            if len(key_path) > 1:
                sub_key = key_path.pop(0)
                return get_nested_value(key_path=key_path, dict_data=dict_data.get(sub_key))
            return dict_data.get(key_path[0])
    return None
