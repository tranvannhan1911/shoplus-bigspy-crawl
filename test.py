import cloudscraper
import requests

def get_bigspy_henull_facebook_ads_list(base_domain, page, token, cookie):
    base_url = "https://"+base_domain
    url = base_url+"/ecom/get-ecom-ads?favorite_app_flag=0&ecom_category=&search_type=1&platform=1&category=&os=0&ads_promote_type=0&geo=VNM&game_play=&game_style=&type=2&page="+ str(page) +"&industry=3&language=&keyword=&sort_field=first_seen&region=&original_flag=0&is_preorder=0&theme=&text_md5=&ads_size=&ads_format=&exclude_keyword=&cod_flag=0&cta_type=&new_ads_flag=0&like_begin=1000&like_end=&comment_begin=&comment_end=&share_begin=&share_end=&position=0&is_hide_advertiser=0&advertiser_key=&dynamic=0&shopping=0&duplicate=0&software_types=&ecom_types=&social_account=&modules=ecomad&page_id=&landing_type=0&is_first=0&page_load_more=1&source_app="

    payload = {}
    headers = {
        'authority': base_domain,
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': token,
        'cookie': cookie,
        'referer': base_url+'/iframe/adspy/facebook/?utm_home=1&token='+token,
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    # response = requests.request("GET", url, headers=headers, data=payload)
    scraper = cloudscraper.create_scraper()
    html = scraper.get("https://www.sneakersnstuff.com/", headers=headers, data=payload).content
    print(html)
    # return response

