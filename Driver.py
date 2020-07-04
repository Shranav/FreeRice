from selenium import webdriver
import time
import random
import math


def get_rice():
    with open('RiceCount', "r") as handle:
        rice = handle.read().strip()
    return rice


def update_rice(count=10):
    rice = int(get_rice())
    with open('RiceCount', 'w') as handle:
        handle.write(str(rice + count))


def runs():
    runtime = int(input("How long should the program run in mins? "))
    return runtime


def get_answers(driver, question):
    ans = []
    for i in range(2, 6):  # Gather all 4 answers
        elemen = driver.find_element_by_xpath(
            '/html/body/div/section/div/div[1]'
            '/div/div/div[4]/div[1]/div/div/div'
            '/div/div/div[' + str(i) + ']')
        ans.append(elemen)
    num1 = is_int(question[0])
    num2 = is_int(question[1])
    return num1, num2, ans


def is_int(num, error=False):
    try:
        num = int(num)
    except ValueError:
        if error:
            num = math.floor(num)
        else:
            num = -1
        print("No Integer was found in the question.")
    return num


def error_percent():
    error_p = [True, True, True, True, True,
               False, True, False, True, True,
               True, True, True, True, True]
    choice = random.randrange(0, len(error_p) - 1)  # Introduce random error, at 13/15 % chance of correct
    return error_p[is_int(choice, True)]


def answer_question(ele, drive):
    text = ele.text
    question = text.split(' x ')
    num1, num2, ans = get_answers(drive, question)
    if num1 != -1 and num2 != -1:
        calc_ans = str(num1 * num2)
        for answer in ans:
            if answer.text == calc_ans:
                if error_percent():
                    answer.click()
                    update_rice()
                    break
                else:
                    if ans[2].text == calc_ans:
                        update_rice()
                    ans[2].click()
                    print("Error Percent")
                time.sleep(2)


def loop(driver):
    run_num = runs()
    while run_num > 0:
        time.sleep(random.randrange(4, 8))  # Simulates time to read question
        element = driver.find_element_by_class_name("card-title")
        answer_question(element, driver)
        run_num -= 1


def main(url, path):
    driver = webdriver.Firefox(executable_path=path)  # Run Selenium
    driver.get(url)
    loop(driver)
    driver.quit()


if __name__ == '__main__':
    url1 = 'https://freerice.com/categories/multiplication-table'
    path1 = r'C:\Users\owner\Downloads\geckodriver.exe'
    main(url1, path1)

