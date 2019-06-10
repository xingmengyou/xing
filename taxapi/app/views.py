import re
from django.shortcuts import render
from app.models import WjzInfo
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import tkinter
import tkinter.messagebox
from selenium.webdriver.support.wait import WebDriverWait


# Create your views here.

def isalarter(driver):
    result = EC.alert_is_present()(driver)
    if result:
        driver.switch_to.alert.accept()


def hello(request):
    cid = request.GET.get('cid')
    data = WjzInfo.objects.get(id=cid)
    data.name = '大项目'
    data.save()
    return render(request, 'ss.html',context= {'status': '0'})


def report(request):
    cid = request.GET.get('cid')
    data = WjzInfo.objects.get(id=cid)
    driver = webdriver.Ie()
    loginurl = 'http://jcpt.ha-n-tax.gov.cn/web/dzswj/ythclient/mh.html'
    mainurl = 'http://jcpt.ha-n-tax.gov.cn/web/dzswj/taxclient/main.html'
    driver.get(loginurl)
    driver.maximize_window()
    time.sleep(0.5)
    login_span = driver.find_element_by_id('id_mh_login_span')
    driver.execute_script("arguments[0].click();", login_span)
    try:
        while True:
            isalarter(driver)
            c_url = driver.current_url
            if 'login_index.html' in c_url:
                em = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'nsrmc')))
                if em.is_displayed():
                    break
                else:
                    time.sleep(3)
                    continue
            else:
                time.sleep(3)
                continue

    except Exception as e:
        print(e)
        # driver.quit()
        return render(request, 'ss.html', context={'status': '1'})
    else:
        time.sleep(0.5)
        driver.get(mainurl)
        time.sleep(0.5)
        isalarter(driver)
        isalarter(driver)
        main_iframe = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'main_iframe')))
        # 跳转到iframe操作
        driver.switch_to.frame(main_iframe)
        source = driver.page_source
        if 'iframe78282' not in source:
            gxhbs = WebDriverWait(driver, 8).until(EC.visibility_of_element_located((
                By.XPATH, "//a[@title='个性化办税']")))
            driver.execute_script("arguments[0].click();", gxhbs)
            tcyw = driver.find_element_by_xpath("//a[@title='套餐及组合业务']")
            driver.execute_script("arguments[0].click();", tcyw)
            kqybg = driver.find_element_by_xpath("//a[contains(@title,'跨区域事项报告及报验套餐')]")
            driver.execute_script("arguments[0].click();", kqybg)
            time.sleep(3)
            isalarter(driver)
            isalarter(driver)
        driver.switch_to.frame('iframe78282')
        driver.switch_to.frame(driver.find_element_by_class_name('inIframe'))
        driver.switch_to.frame(driver.find_element_by_id('frame0'))
        driver.switch_to.frame('left1')
        # 报告表添加数据
        driver.execute_script('DCellWeb1.SetCellString(2,3,0,"{}")'.format(data.agent))
        driver.execute_script('DCellWeb1.SetCellString(7,3,0,"{}")'.format(data.phone))
        driver.execute_script('DCellWeb1.SetCellString(3,6,0,"{}")'.format(data.address))
        driver.execute_script('DCellWeb1.SetCellString(9,8,0,"{}")'.format(data.unit))
        driver.execute_script('DCellWeb1.SetCellString(1,11,0,"{}")'.format(data.name))
        driver.execute_script('DCellWeb1.SetCellDouble(11,11,0,{} )'.format(data.money))  # 合同金额
        driver.execute_script('DCellWeb1.SetCellString(7,11,0,"{}")'.format(data.begindate))
        driver.execute_script('DCellWeb1.SetCellString(9,11,0,"{}")'.format(data.enddate))
        # ID号
        ywid = driver.find_element_by_id("ID").get_attribute('value')
        print('业务ID:', ywid)
        tkinter.Tk().withdraw()
        tkinter.messagebox.showinfo('业务ID:', ywid)
        data.ywid = ywid
        data.save()
        return render(request, 'ss.html')


def update_jd(request):
    cid = request.GET.get('cid')
    if cid:
        data = WjzInfo.objects.get(ywid=cid)
        try:
            driver = webdriver.Ie()
            driver.maximize_window()
            loginurl = 'http://jcpt.ha-n-tax.gov.cn/web/dzswj/ythclient/mh.html'
            mainurl = 'http://jcpt.ha-n-tax.gov.cn/web/dzswj/taxclient/main.html'
            bljdurl = 'http://wsbsfwt.ha-n-tax.gov.cn/taxclient/wssq/zhcx/bsjdcx/bsjdcx_index.html'
            driver.get(loginurl)
            time.sleep(0.5)
            login_span = driver.find_element_by_id('id_mh_login_span')
            driver.execute_script("arguments[0].click();", login_span)
            while True:
                isalarter(driver)
                c_url = driver.current_url
                if 'login_index.html' in c_url:
                    em = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'nsrmc')))
                    if em.is_displayed():
                        break
                    else:
                        time.sleep(3)
                        continue
                else:
                    time.sleep(3)
                    continue
            # time.sleep(0.5)
            # driver.get(mainurl)
            # time.sleep(0.5)
        except Exception as e:
            print(e)
            return render(request, 'ss.html', context={'status': '1'})
        else:
            time.sleep(0.5)
            driver.get(mainurl)
            time.sleep(0.5)
            driver.get(bljdurl)
            time.sleep(1)
            rq_q = driver.find_element_by_id('SQRQ_Q')
            rq_q.clear()
            rq_q.send_keys(data.begindate)
            # rq_z = driver.find_element_by_id('SQRQ_Z')
            # rq_z.clear()
            # rq_z.send_keys(data.begindate)
            time.sleep(0.5)
            search = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//span[@class="wep_cxzx_btn wep_cxzx_btn2 wdl_mr0"]')))
            driver.execute_script("arguments[0].click();", search)
            time.sleep(2)
            # 办理进度
            try:
                data.jd = driver.find_element_by_xpath(
                    '//a[text()="{}"]/../../td[5]/span'.format(cid)).text
                print('当前进度:', data.jd)
                tkinter.Tk().withdraw()
                tkinter.messagebox.showinfo('办理进度', data.jd)
                data.save()
            except Exception as e:
                print(e)
                print('无此报告,请重新申请')
                return render(request, 'ss.html', context={'status': '2'})

            else:
                # 进度完成,获取文书地址
                if '已完成' in data.jd:
                    ckws = driver.find_element_by_xpath('//a[text()="{}"]/../../td[6]/a'.format(
                        cid)).get_attribute('href')
                    lcslid = re.findall(r'\"(.*?)\"', ckws)[0]
                    js = 'window.open("http://wsbsfwt.ha-n-tax.gov.cn/taxclient/wssq/ywsqcx/wsList.htm' \
                         'l?LCSLID={}")'.format(lcslid)
                    print(js)
                    driver.execute_script(js)
                    time.sleep(2)
                    c_h = driver.window_handles[-1]
                    driver.switch_to.window(c_h)
                    print(driver.current_url)
                    data.managenum = driver.find_element_by_xpath('//table[@id="tbList"]//tr/td[4]/span').text
                    print('管理编号:', data.managenum)
                    ck = driver.find_element_by_link_text('查看')[0]
                    driver.execute_script("arguments[0].click();", ck)
                    time.sleep(2)
                    w_h = driver.window_handles[-1]
                    driver.switch_to.window(w_h)
                    tkinter.Tk().withdraw()
                    tkinter.messagebox.showinfo('提示', '请稍等.....')
                    data.documenturl = driver.current_url
                    print('文书地址:', data.documenturl)

                    # while True:
                    #     source = driver.page_source
                    #     if '跨区域涉税事项报告表' not in source:
                    #         time.sleep(2)
                    #     else:
                    #         db_item.validity = driver.find_element_by_xpath('//tbody/tr[14]/td[2]/p').text
                    #         print('有效期:', validity)
                    #         break
                    data.save()
                return render(request, 'ss.html')
    else:
        return render(request, 'ss.html')







