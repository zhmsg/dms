/**
 * Created by zhouhenglc on 2019/11/29.
 */
 var policies_key = "use_policies";

function save_policies(policies)
 {
    _save_session_storage(policies_key, policies);
 }

 function get_policies()
 {
     var value = _get_session_storage(policies_key);
     if(value == null){
         var url = "/user/policies";
         my_request2(url, "GET", null, function(data){
             save_policies(data);
             value = data;
         });
     }
     return value;
 }

 function verify_policy(m_key, p_key)
 {
    var policies = get_policies();
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