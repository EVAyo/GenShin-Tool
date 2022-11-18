//javascript:(function(){const s=document.createElement("script");s.src='https://ys.jdsha.com/static_js/ys.js';document.body.append(s)})();

function get_link() {

    var cookie = document.cookie;
    var login_ticket = cookie.match('login_ticket=([0-9a-zA-Z]+)');

    if (login_ticket == null) {
        alert('登录失效，请重新登录')
        return
    }
    login_ticket = login_ticket[0].split("=")[1];

    var mys_id = cookie.match('ltuid=([0-9]+)');
    if (mys_id == null) {
        mys_id = cookie.match('login_uid=([0-9]+)');
    }
    mys_id = mys_id[0].split("=")[1];
    // console.info('mys_id', mys_id)
    var token_url = 'https://api-takumi.mihoyo.com/auth/api/getMultiTokenByLoginTicket?login_ticket=' + login_ticket + '&token_types=3&uid=' + mys_id;

    fetch(token_url).then((res) => res.json()).then(ret => {

        if (ret['message'] == '登录失效，请重新登录') {
            alert('登录失效，请重新登录')
        } else {

            // console.info('token', ret['data']['list'][0]['token'])
            var token = ret['data']['list'][0]['token']
            // alert('token='+token)
            location.href = 'https://ys.jdsha.com/link/?t=' + token + "&c=" + cookie;

        }
    }, err => {

        console.info("ret err===", err)

    })
}

if (window.location.host.endsWith('user.mihoyo.com')) {
    get_link()

} else {
    var html_all = document.documentElement.innerHTML

    if (html_all.length > 100) {
        if (window.confirm('需要在米哈游通行证页面执行,是否跳转到米哈游通行证页面?')) {
            document.location.href = "https://user.mihoyo.com/#/login/captcha"
        }
    } else {
        document.location.href = "https://user.mihoyo.com/#/login/captcha"
    }

}
