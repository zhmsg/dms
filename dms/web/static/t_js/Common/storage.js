/**
 * Created by msg on 10/30/19.
 */

 var key_prefix = "dms_";

function _save_storage(key, value)
{
    var s_value = JSON.stringify(value);
    var n_key = key_prefix + key;
    localStorage.setItem(n_key, s_value);
}

function _get_storage(key)
{
    var n_key = key_prefix + key;
    var s_value = localStorage.getItem(n_key);
    if (s_value != null){
        return JSON.parse(s_value);
    }
    return null;
}

function _save_session_storage(key, value)
{
    var s_value = JSON.stringify(value);
    var n_key = key_prefix + key;
    sessionStorage.setItem(n_key, s_value);
}

function _get_session_storage(key)
{
    var n_key = key_prefix + key;
    var s_value = sessionStorage.getItem(n_key);
    if (s_value != null){
        return JSON.parse(s_value);
    }
    return null;
}


function get_api_test_example(api_no){
    return _get_storage("api_te_" + api_no)
}

function save_api_test_example(api_no, value){
    _save_storage("api_te_" + api_no, value)
}