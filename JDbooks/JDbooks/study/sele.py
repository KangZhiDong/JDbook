from selenium import webdriver
#import selenium
driver = webdriver.PhantomJS()
driver.get("http://item.jd.com/11678007.html")
#content = driver.find_elements_by_class_name('book-detail-content').extract()
#driver.manage().timeouts().implicitlyWait(1, TimeUnit.SECONDS);
content = driver.find_element_by_xpath('//*[@id="detail-tag-id-6"]/div[2]/div').text
print content
driver.close()
