from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import  Response
from selenium import webdriver
from selenium.webdriver.common.by import By
from linkedin_scraper import Person, actions

from bs4 import BeautifulSoup as bs
import time
import pandas as pd

from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# from parsel import Selector


# Create your views here.
class Automate(APIView):
    def get(self, request):
        return Response({'message':'this is my message'})
    def post(self, request):
        print(request.data)
        payload = request.data
        browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')

        browser.get('https://www.linkedin.com')
        username = browser.find_element(By.ID,"session_key")
        username.send_keys(payload['email'])

        password = browser.find_element(By.ID,"session_password")

        # send_keys() to simulate key strokes
        password.send_keys(payload['password'])
        # log_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')

        # # locate submit button by_class_id
        # log_in_button = driver.find_element_by_class_id('login submit-button')

        # locate submit button by_xpath
        log_in_button = browser.find_element_by_xpath('//*[@type="submit"]')

        # .click() to mimic button click
        log_in_button.click()
        # send_keys() to simulate key strokes
        
        # actions.login(driver, payload['email'], payload['password']) # if email and password isnt given, it'll prompt in terminal
        browser.find_element_by_xpath("//span[.='Views of your post']").click()
        

        # scrapping the posts


        #Simulate scrolling to capture all posts
        SCROLL_PAUSE_TIME = 1.5

        # Get scroll height

                
        #Simulate scrolling to capture all posts
        SCROLL_PAUSE_TIME = 1.5

        # Get scroll height
        last_height = browser.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        elements = ui.WebDriverWait(browser, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "social-details-social-counts__comments")))
        for el in elements:
            
            action = ActionChains(browser)
            action.move_to_element(el).perform()
            el.click()

        time.sleep(5)

        company_page = browser.page_source   



        # #Import exception check for message popups (not needed atm)
        # from selenium.common.exceptions import NoSuchElementException
        # try:
        #     if browser.find_element_by_class_name('msg-overlay-list-bubble--is-minimized') is not None:
        #         pass
        # except NoSuchElementException:
        #     try:
        #         if browser.find_element_by_class_name('msg-overlay-bubble-header') is not None:
        #             browser.find_element_by_class_name('msg-overlay-bubble-header').click()
        #     except NoSuchElementException:
        #         pass


        #Use Beautiful Soup to get access tags
        linkedin_soup = bs(company_page.encode("utf-8"), "html")
        linkedin_soup.prettify()
        # test = linkedin_soup.findAll("li", {"class": "social-details-social-counts__comments social-details-social-counts__item"})
        # print('the test length', len(test))

        #Find the post blocks
        containers = linkedin_soup.findAll("div",{"class":"occludable-update ember-view"})

        # container = containers[0].find("div","feed-shared-update-v2__description-wrapper ember-view")


        # Lists that we will iterate to
        post_dates = []
        post_texts = []
        post_likes = []
        post_comments = []
        video_views = []
        media_links = []
        media_type = []
        comments=[]

        #Looping through the posts and appending them to the lists
        for container in containers:
            
            try:
                posted_date = container.find("span",{"class":"visually-hidden"})
                text_box = container.find("div",{"class":"feed-shared-update-v2__description-wrapper ember-view"})
                text = text_box.find("span",{"dir":"ltr"})
                new_likes = container.findAll("li", {"class":"social-details-social-counts__reactions social-details-social-counts__item"})
                new_comments = container.findAll("li", {"class": "social-details-social-counts__comments social-details-social-counts__item"})
                # print('length of comment is', len(new_comments), type(len(new_comments)))
                        
                commentor_name = container.findAll("span", {"class": "comments-post-meta comments-comment-item__post-meta"})
                print('the length of comment', len(commentor_name))
                try:

                    commentor_name = container.findAll("div", {"class": "feed-shared-text relative"})
                    print('inside text',len(commentor_name))
                    dat = []
                    for e in commentor_name:
                        print('commentor name',e.text.strip())  
                        dat.append(e.text.strip())
                    comments.append(dat)
                except:
                    print('no text found')




                
                #Appending date and text to lists
                post_dates.append(posted_date.text.strip())
                post_texts.append(text_box.text.strip())


                #Determining media type and collecting video views if applicable
                try:
                    video_box = container.findAll("div",{"class": "feed-shared-update-v2__content feed-shared-linkedin-video ember-view"})
                    video_link = video_box[0].find("video", {"class":"vjs-tech"})
                    media_links.append(video_link['src'])
                    media_type.append("Video")
                except:
                    try:
                        image_box = container.findAll("div",{"class": "feed-shared-image__container"})
                        image_link = image_box[0].find("img", {"class":"ivm-view-attr__img--centered feed-shared-image__image feed-shared-image__image--constrained lazy-image ember-view"})
                        media_links.append(image_link['src'])
                        media_type.append("Image")
                    except:
                        try:
                            image_box = container.findAll("div",{"class": "feed-shared-image__container"})
                            image_link = image_box[0].find("img", {"class":"ivm-view-attr__img--centered feed-shared-image__image lazy-image ember-view"})
                            media_links.append(image_link['src'])
                            media_type.append("Image")
                        except:
                            try:
                                article_box = container.findAll("div",{"class": "feed-shared-article__link-container"})
                                article_link = article_box[0].find("a", {"class":"feed-shared-article__image-link tap-target app-aware-link ember-view"})
                                media_links.append(article_link['href'])
                                media_type.append("Article")
                            except:
                                try:
                                    poll_box = container.findAll("div",{"class": "feed-shared-update-v2__content overflow-hidden feed-shared-poll ember-view"})
                                    media_links.append("None")
                                    media_type.append("Other (Shared Post/Poll, etc.)")
                                except:
                                    media_links.append("None")
                                    media_type.append("Unknown")



                #Getting Video Views. (The folling three lines prevents class name overlap)
                view_container2 = set(container.findAll("li", {'class':["social-details-social-counts__item"]}))
                view_container1 = set(container.findAll("li", {'class':["social-details-social-counts__reactions","social-details-social-counts__comments social-details-social-counts__item"]}))
                result = view_container2 - view_container1

                view_container = []
                for i in result:
                    view_container += i

                try:
                    video_views.append(view_container[1].text.strip().replace(' Views',''))

                except:
                    video_views.append('N/A')

                
                #Appending likes and comments if they exist
                try:
                    post_likes.append(new_likes[0].text.strip())
                except:
                    post_likes.append(0)
                    pass

                try:
                    post_comments.append(new_comments[0].text.strip())    
                    # print('comment',new_comments[0].text.strip())                       
                except:                                                           
                    post_comments.append(0)
                    pass
            
            except:
                pass

            
        # #Cleaning the dates
        # cleaned_dates = []
        # for i in post_dates:
        #     d = str(i[0:3]).replace('\n\n', '').replace('•','').replace(' ', '')
        #     cleaned_dates += [d]


        #Stripping non-numeric values
        comment_count = []
        for i in post_comments:
            s = str(i).replace('Comment','').replace('s','').replace(' ','')
            comment_count += [s]


            
        #Constructing Pandas Dataframe
        data = {
            "Date Posted": post_dates,
            "Media Type": media_type,
            "Post Text": post_texts,
            "Post Likes": post_likes,
            "Post Comments": comment_count,
            "Video Views": video_views,
            "Media Links": media_links,
            "Comments":comments
        }
        print(data)

        df = pd.DataFrame(data)
        return Response({'message':df,'data':data})
