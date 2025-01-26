commands to run:

pip install -r requirements.txt

uvicorn scraping..main:app --reload 


CURL to test the API
curl --location --request POST 'http://127.0.0.1:8000/scrape?limit_pages=1' \
--header 'Authorization: Bearer namans_token'

NOTES:
--- In the above curl you can send the number of pages you want to scrape by updating the param:limit_pages.
--- Make sure when running (uvicorn scraping..main:app --reload ) command, you are in the app directory.