# Health Survey Auto Answer
This cdoe is used to answer the health survey automatically.

## Usage
There are two ways to use it.
1. Run locally
2. Run on heroku using heroku scheduler

I recommend you to use the first one.

### How to run locally
1. Clone this repository.
2. Set up chromedriver.(The configuration method differs depending on the OS.)
3. `pip install -r requirements.txt`
4. Set the environment variables
    - required
        - export HEALTH_SERVEY_URL="https://..."
        - export EMAIL="your email address"
        - export PASSWORD="your password"
    - optional
        - export CHROME_DRIVER_PATH="path to chromedriver"
        - export ACTIVITY_NAME="activity name"
        - export IS_GET_EMAIL_RECEIPT="true or false"
        - export IS_DETERMINATE_BY_BIZDAY="true or false"
        - export IS_ATTEND_SCHOOL="true or false"
5. `python main.py`
6. (Set up to run periodically using the schedule function)

### How to run on heroku
1. Clone this repository.
2. Set up git, heroku locally.
3. `cd this repository`
4. `heroku create app-name`
5. `git remote add heroku your-heroku-app-url`
6. `git push heroku master`
7. `heroku addons:add scheduler:standard` (You may need to register your credit card.)
8. Set up heroku scheduler from the heroku scheduler page.
9. Add buildpacks(after add buildpacks, you need to redeploy the app.)
    - heroku/python
    - https://github.com/heroku/heroku-buildpack-google-chrome
    - https://github.com/heroku/heroku-buildpack-chromedriver
10. Set the environment variables
    - required
        - HEALTH_SERVEY_URL="https://..."
        - EMAIL="your email address"
        - PASSWORD="your password"
        - CHROME_DRIVER_PATH="/app/.chromedriver/bin/chromedriver"
    - optional
        - ACTIVITY_NAME="activity name"
        - IS_GET_EMAIL_RECEIPT="true or false"
        - IS_DETERMINATE_BY_BIZDAY="true or false"
        - IS_ATTEND_SCHOOL="true or false"
        - LINE_NOTIFY_TOKEN="your line notify token"