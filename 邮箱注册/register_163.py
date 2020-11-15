import utils
import time


# 将用户密码插入mysql
def save_email(conn, name, pwd, phone):
    curr_time = utils.get_curr_time()
    insert_sql = "INSERT INTO email_163(user_name, pass_word, phone, create_time) " \
                 "VALUES ('{0}', '{1}', '{2}', '{3}')".format(name + '@163.com', pwd, phone, curr_time)
    utils.execute_sql(conn, insert_sql)


# 注册163邮箱
def register_163():
    try:
        driver = utils.init_chrome()
        # 发送请求 打开注册页面
        driver.get('https://mail.163.com/register/index.htm?from=163mail')
        # 随机生成用户名和密码
        user_name = utils.get_one_letters() + utils.random_str(11)
        pass_word = utils.get_one_letters() + utils.random_str(6) + utils.get_one_number()

        # 定位元素框 填写用户名密码
        driver.find_element_by_id('username').send_keys(user_name)
        # 用户名是否有效
        user_name_tip_div = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[2]/div[1]/div[3]')
        tip_display = user_name_tip_div.is_displayed()
        if tip_display:
            return None, None, None

        # 填写密码
        driver.find_element_by_id('password').send_keys(pass_word)
        # 密码是否有效
        pwd_tip_div = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[2]/div[2]/div')
        pwd_tip = pwd_tip_div.get_attribute('innerText')
        err_msg = '密码过于简单，请尝试“字母+数字”的组合'
        if pwd_tip == err_msg:
            return None, None, None

        # 对接接码平台 获取电话和验证码
        phone = utils.get_phone_no('简书')
        driver.find_element_by_id("phone").send_keys(phone)
        time.sleep(3)
        # 电话是否有效
        phone_tip_div = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[2]/div[3]/div[2]')
        phone_tip = phone_tip_div.get_attribute('innerText')
        err_msg = '该手机号关联帐号太多'
        if phone_tip == err_msg:
            # 拉黑当前手机号并退出
            utils.block_phone_no(phone)
            return None, None, None

        # 点击同意服务条款
        driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[2]/div[4]/span').click()
        time.sleep(2)

        # 点击手动发送
        driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[2]/div[3]/div[1]/div[1]/div[2]/a').click()
        time.sleep(3)
        show = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[2]/div[3]/div[1]/div[2]').is_displayed()
        if show:
            # 获取收信人号码
            to_phone_span = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[2]/div[3]/div[1]/div[2]/div[2]/p[2]/span')
            to_phone = to_phone_span.get_attribute('innerText')
            # 获取要发送的内容
            send_msg_span = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[2]/div[3]/div[1]/div[2]/div[2]/p[1]/span')
            send_msg = send_msg_span.get_attribute('innerText')
            # 发送验证短信
            utils.send_msg(phone, to_phone, send_msg)
        else:
            return None, None, None
        time.sleep(5)
        # 点击立即注册按钮
        driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[2]/div[5]/a[1]').click()
        time.sleep(3)
        ssm_tip_div = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[2]/div[3]/div[2]')
        ssm_tip = ssm_tip_div.get_attribute('innerText')
        err_msg = '系统未收到短信，请检查手机号是否正确或重新发送短信'
        if ssm_tip == err_msg:
            print(err_msg)
            return None, None, None

        return user_name, pass_word, phone

    except Exception as e:
        print('=========注册失败,执行下一个任务=========')
        print(e)
    finally:
        driver.close()


if __name__ == '__main__':
    # connect mysql
    conn = utils.get_db_conn('localhost', 3306, 'root', 'root', 'test')
    # login ssm
    utils.login_ssm()
    time.sleep(3)
    # register begin
    for i in range(1):
        user_name, pass_word, phone = register_163()
        if user_name is not None and pass_word is not None and phone is not None:
            save_email(conn, user_name, pass_word, phone)
    # close mysql connect
    conn.close()
    utils.login_ssm_out()
