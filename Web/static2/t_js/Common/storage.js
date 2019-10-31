/**
 * Created by msg on 10/30/19.
 */

 var key_prefix = "dms_"
 var policies_key = "use_policies"


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

 function save_policies(policies)
 {
    _save_session_storage(policies_key, policies)
 }

 function get_policies()
 {
    return _get_session_storage(policies_key)
 }

 function verify_policy(m_key, p_key)
 {
    var policies = get_policies()
    console.info(policies);
    if(policies == null){
        return false;
    }
    var role = 0;
    if(policies.hasOwnProperty("role")){
        role = policies['role'];
    }
    if(role >= 10){
        return true;
    }
    if(!policies.hasOwnProperty("policies")){
        return false
    }

    var o_policies = policies["policies"];

    if(!o_policies.hasOwnProperty(m_key)){
        return false;
    }
    var m_values = o_policies[m_key];
    if(m_values.indexOf(p_key) >= 0)
    {
        return true;
    }
    return false;
 }