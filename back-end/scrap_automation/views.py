from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import  Response
from selenium import webdriver
from selenium.webdriver.common.by import By

# from parsel import Selector


# Create your views here.
class Automate(APIView):
    def get(self, request):
        return Response({'message':'this is my message'})
    def post(self, request):
        print(request.data)
        payload = request.data
        driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')

        driver.get('https://www.linkedin.com')
        username = driver.find_element(By.ID,"session_key")
        username.send_keys(payload['email'])

        password = driver.find_element(By.ID,"session_password")

        # send_keys() to simulate key strokes
        password.send_keys(payload['password'])
        # log_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')

        # # locate submit button by_class_id
        # log_in_button = driver.find_element_by_class_id('login submit-button')

        # locate submit button by_xpath
        log_in_button = driver.find_element_by_xpath('//*[@type="submit"]')

        # .click() to mimic button click
        log_in_button.click()
        # send_keys() to simulate key strokes
        

        return Response({'message':'you have logged in'})
