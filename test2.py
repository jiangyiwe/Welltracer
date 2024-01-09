from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

# 设置Selenium WebDriver
options = Options()
options.headless = False  # 使浏览器可见
browser = webdriver.Firefox(options=options)

try:
    # 目标网址, 这里以Paris为例
    location = "paris"
    availabilities = "3"
    url = f"https://www.doctolib.fr/medecin-generaliste/{location}?availabilities={availabilities}"

    # 使用Selenium打开网页
    browser.get(url)

    # 等待特定元素加载完成
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".dl-search-result-presentation"))
    )

    # 解析网页
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    # 提取医生的名字和可用时间段
    doctors_info = []

    # 找到外层的 'col-8 col-padding search-results-col-list' 容器
    search_results_list = soup.find_all("div", class_="col-8 col-padding search-results-col-list")

    for results_list in search_results_list:
        # 在每个外层容器中寻找 'dl-layout-container'
        layout_containers = results_list.find_all("div", class_="dl-layout-container")
        for layout_container in layout_containers:
            # 对每个医生信息块进行遍历
            doc_blocks = layout_container.find_all("div", class_="dl-layout-item dl-layout-size-xs-12")
            for doc_block in doc_blocks:
                presentation_container = doc_block.find("div", class_="dl-search-result-presentation")
                if presentation_container:
                    name_section = presentation_container.find("h3",
                                                               class_="dl-text dl-text-body dl-text-regular dl-text-s dl-text-primary-110")
                    name = name_section.text.strip() if name_section else "Name not found"
                else:
                    continue  # 如果没有找到名称容器则跳过

                # 查找该医生对应的可用时间段
                calendar_container = doc_block.find("div", class_="dl-search-result-calendar")
                time_slots = []
                if calendar_container:
                    # 遍历每个'日'的容器
                    days_containers = calendar_container.find_all("div", class_="availabilities-day")
                    for day_container in days_containers:
                        # 在每个'日'的容器中遍历可用时间段
                        slots = day_container.find_all("div", class_="availabilities-slot")
                        for slot in slots:
                            time = slot.get("aria-label", "No time found").strip()
                            time_slots.append(time)

                if name != "Name not found" and time_slots:
                    doctors_info.append({"name": name, "availability": time_slots})

    # 打印医生名字及可用时间段
    for doctor in doctors_info:
        print(f"{doctor['name']} available at {doctor['availability']}")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    browser.quit()