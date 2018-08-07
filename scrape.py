from selenium import webdriver
import pandas as pd
import time

if __name__ == "__main__":
    driver = webdriver.Firefox()

    driver.get('http://trinitytiming.com/results/#/race/J6PDAU/1/results/ALL')

    time.sleep(7)

    tbl = driver.find_element_by_id('table-results')
    df = pd.read_html(tbl.get_attribute('outerHTML'))
    fname = 'data.csv'
    df[0].to_csv(fname)

    for n in range(2,44):
        print('Starting ' + str(n))
        driver.find_element_by_xpath("//a[text()='" + str(n) + "']").click()
        time.sleep(3)
        tbl = driver.find_element_by_id('table-results')

        with open(fname, 'a') as f:
            pd.read_html(tbl.get_attribute('outerHTML'))[0].to_csv(f, header=False)

    print('Done!')