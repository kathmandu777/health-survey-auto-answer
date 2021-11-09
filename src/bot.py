from selenium import webdriver
import os
from time import sleep
import random
import jpbizday
import datetime
from .constants import (
    DEFAULT_IS_DETERMINATE_BY_BIZDAY,
    DEFAULT_IS_ATTEND_SCHOOL,
    DEFAULT_IS_GET_EMAIL_RECEIPT,
    MAX_BODY_TEMPERATURE,
    MIN_BODY_TEMPERATURE,
)
import requests


class HealthSurveyAutoAnswerBot:
    SLEEP_TIME = 10
    EMAIL_INPUT_BOX_ID = "i0116"
    EMAIL_SUBMIT_BUTTON_ID = "idSIButton9"
    PASSWORD_INPUT_BOX_ID = "i0118"
    PASSWORD_SUBMIT_BUTTON_ID = "idSIButton9"
    STAY_SIGNED_IN_YES_SUBMIT_BUTTON_ID = "idSIButton9"
    STAY_SIGNED_IN_NO_SUBMIT_BUTTON_ID = "idBtn_Back"
    BODY_TEMPERATURE_INPUT_BOX_XPATH = "//*[@id='form-container']/div/div/div[1]/div/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div/input"
    NO_SYMPTOMS_RADIO_BUTTON_XPATH = "//*[@id='form-container']/div/div/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div/label/input"
    ATTEND_SCHOOL_RADIO_BUTTON_XPATH = "//*[@id='form-container']/div/div/div[1]/div/div[1]/div[2]/div[2]/div[3]/div/div[2]/div/div[1]/div/label/input"
    ABSENT_SCHOOL_RADIO_BUTTON_XPATH = "//*[@id='form-container']/div/div/div[1]/div/div[1]/div[2]/div[2]/div[3]/div/div[2]/div/div[2]/div/label/input"
    ATTEND_EXTRA_ACTIBITY_RADIO_BUTTON_XPATH = "//*[@id='form-container']/div/div/div[1]/div/div[1]/div[2]/div[2]/div[4]/div/div[2]/div/div[1]/div/label/input"
    ABSENT_EXTRA_ACTIBITY_RADIO_BUTTON_XPATH = "//*[@id='form-container']/div/div/div[1]/div/div[1]/div[2]/div[2]/div[4]/div/div[2]/div/div[2]/div/label/input"
    ACTIVITY_NAME_INPUT_BOX_XPATH = "//*[@id='form-container']/div/div/div[1]/div/div[1]/div[2]/div[2]/div[5]/div/div[2]/div/div/input"
    SEND_ME_AN_EMAIL_RECEIPT_CHECKBOX_BUTTON_XPATH = "//*[@id='form-container']/div/div/div[1]/div/div[1]/div[2]/div[3]/div/div/label/input"
    SURVEY_SUBMIT_BUTTON_XPATH = "//*[@id='form-container']/div/div/div[1]/div/div[1]/div[2]/div[4]/div[1]/button/div"

    def __init__(self) -> None:
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--disable-notifications")
        self.options.add_argument('--proxy-server="direct://"')
        self.options.add_argument("--proxy-bypass-list=*")
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--disable-application-cache")
        self.browser = webdriver.Chrome(
            options=self.options,
        )

        self.run()

    def login(self, email: str, password: str) -> None:
        self.browser.find_element_by_id(self.EMAIL_INPUT_BOX_ID).send_keys(email)
        self.browser.find_element_by_id(self.EMAIL_SUBMIT_BUTTON_ID).click()
        sleep(self.SLEEP_TIME)

        self.browser.find_element_by_id(self.PASSWORD_INPUT_BOX_ID).send_keys(password)
        self.browser.find_element_by_id(self.PASSWORD_SUBMIT_BUTTON_ID).click()
        sleep(self.SLEEP_TIME)

        self.browser.find_element_by_id(
            self.STAY_SIGNED_IN_YES_SUBMIT_BUTTON_ID
        ).click()
        sleep(self.SLEEP_TIME)

    def get_body_temperature(
        self,
        max_body_temperature: float = MAX_BODY_TEMPERATURE,
        min_body_temperature: float = MIN_BODY_TEMPERATURE,
    ) -> str:
        return str(random.uniform(min_body_temperature, max_body_temperature))[:4]

    def answer_health_survey(
        self,
        is_get_email_receipt: bool,
        is_determinate_by_bizday: bool,
        is_attend_school: bool,
    ) -> None:
        self.browser.get(os.environ.get("HEALTH_SERVEY_URL"))
        sleep(self.SLEEP_TIME)

        self.login(os.environ.get("EMAIL", ""), os.environ.get("PASSWORD", ""))

        self.browser.find_element_by_xpath(
            self.BODY_TEMPERATURE_INPUT_BOX_XPATH
        ).send_keys(self.get_body_temperature())
        sleep(self.SLEEP_TIME)

        self.browser.find_element_by_xpath(self.NO_SYMPTOMS_RADIO_BUTTON_XPATH).click()
        sleep(self.SLEEP_TIME)

        if (is_determinate_by_bizday and jpbizday.is_bizday(datetime.date.today())) or (
            not is_determinate_by_bizday and is_attend_school
        ):
            self.browser.find_element_by_xpath(
                self.ATTEND_SCHOOL_RADIO_BUTTON_XPATH
            ).click()
            sleep(self.SLEEP_TIME)

            if os.environ.get("ACTIVITY_NAME", False):
                self.browser.find_element_by_xpath(
                    self.ATTEND_EXTRA_ACTIBITY_RADIO_BUTTON_XPATH
                ).click()
                sleep(self.SLEEP_TIME)

                self.browser.find_element_by_xpath(
                    self.ACTIVITY_NAME_INPUT_BOX_XPATH
                ).send_keys(os.environ.get("ACTIVITY_NAME"))
                sleep(self.SLEEP_TIME)
            else:
                self.browser.find_element_by_xpath(
                    self.ABSENT_EXTRA_ACTIBITY_RADIO_BUTTON_XPATH
                ).click()
                sleep(self.SLEEP_TIME)
        else:
            self.browser.find_element_by_xpath(
                self.ABSENT_SCHOOL_RADIO_BUTTON_XPATH
            ).click()
            sleep(self.SLEEP_TIME)

        if is_get_email_receipt:
            self.browser.find_element_by_xpath(
                self.SEND_ME_AN_EMAIL_RECEIPT_CHECKBOX_BUTTON_XPATH
            ).click()
            sleep(self.SLEEP_TIME)

        self.browser.find_element_by_xpath(self.SURVEY_SUBMIT_BUTTON_XPATH).click()
        sleep(self.SLEEP_TIME)

        self.browser.quit()

    def run(self) -> None:
        is_get_email_receipt = (
            os.environ["IS_GET_EMAIL_RECEIPT"].lower() == "true"
            if os.environ.get("IS_GET_EMAIL_RECEIPT") is not None
            else DEFAULT_IS_GET_EMAIL_RECEIPT
        )
        is_determinate_by_bizday = (
            os.environ["IS_DETERMINATE_BY_BIZDAY"].lower() == "true"
            if os.environ.get("IS_DETERMINATE_BY_BIZDAY") is not None
            else DEFAULT_IS_DETERMINATE_BY_BIZDAY
        )
        is_attend_school = (
            os.environ["IS_ATTEND_SCHOOL"].lower() == "true"
            if os.environ.get("IS_ATTEND_SCHOOL") is not None
            else DEFAULT_IS_ATTEND_SCHOOL
        )
        try:
            self.answer_health_survey(
                is_get_email_receipt=is_get_email_receipt,
                is_determinate_by_bizday=is_determinate_by_bizday,
                is_attend_school=is_attend_school,
            )
        except Exception as e:
            self.line_notify(e)
            self.line_notify(
                "The above error occurred and could not be answered normally. Please use the following link to answer it yourself. "
                + str(os.environ.get("HEALTH_SERVEY_URL"))
            )
            print(e)

    def line_notify(self, message: str) -> None:
        line_notify_token = os.environ.get("LINE_NOTIFY_TOKEN", "")
        line_notify_url = "https://notify-api.line.me/api/notify"
        data = {"message": message}
        headers = {"Authorization": "Bearer " + line_notify_token}
        requests.post(line_notify_url, data=data, headers=headers)
