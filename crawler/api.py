import requests
import json

def get_bigspy_ads_list(token, page):
    url = "https://bigspy.com/ecom/get-ecom-ads?favorite_app_flag=0&ecom_category=&search_type=1&platform=1&category=0&os=0&ads_promote_type=0&geo=VNM&game_play=0&game_style=&type=&page="+str(page)+"&industry=3&language=&keyword=&sort_field=first_seen&region=&original_flag=0&is_preorder=0&theme=&text_md5=&ads_size=&ads_format=&exclude_keyword=&cod_flag=0&cta_type=0&new_ads_flag=0&like_begin=1000&like_end=&comment_begin=&comment_end=&share_begin=&share_end=&position=0&is_hide_advertiser=0&advertiser_key=&dynamic=0&shopping=0&duplicate=0&software_types=&ecom_types=&social_account=&modules=ecomad&page_id=&landing_type=0&is_first=0&page_load_more=1&source_app="

    payload={}
    headers = {
    'authority': 'bigspy.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': token,
    'cookie': 'cf_clearance=hqboDiQr4HFISbB7OX2rwLs0KyyWbCdZaZ54C7wVR1E-1681833662-0-250; sbox-l=en; sbox-guid=MTY4MTgzMzY2OXw1MzF8OTk3NjQ4MzE4; _csrf=6ae3d992aa505207ab7f3da555709072a784c931fc0fad7b3af5e7137040362ca%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%227mI9QUtr1gl9GhsZsnuxYcYG-FhR3UhH%22%3B%7D; _uab_collina=168183366964165489189401; anonymous_user_id=4f7a495011f349376caa5989cd3978eb; _trackUserId=G-1681833670000; _ga=GA1.2.650790373.1681833671; _gid=GA1.2.1430911597.1681833671; crisp-client%2Fsession%2Febd7cf0f-b1ee-4a4e-a4ce-8064999c1331=session_4e3077e9-9013-4afa-8e6d-8ebf566cb320; hy_data_2020_id=18795193f87cc0-00ec7cbb30e87d-26031b51-2073600-18795193f882217; hy_data_2020_js_sdk=%7B%22distinct_id%22%3A%2218795193f87cc0-00ec7cbb30e87d-26031b51-2073600-18795193f882217%22%2C%22site_id%22%3A240%2C%22user_company%22%3A87%2C%22props%22%3A%7B%7D%2C%22device_id%22%3A%2218795193f87cc0-00ec7cbb30e87d-26031b51-2073600-18795193f882217%22%7D; sajssdk_2020_cross_new_user=1; zbase_popup_497=4e7780ace6cc2831e91974d1a549cb0307a0a70f421af346676cf7ef2f0509dba%3A2%3A%7Bi%3A0%3Bs%3A15%3A%22zbase_popup_497%22%3Bi%3A1%3Bs%3A10%3A%22isPopup497%22%3B%7D; is_first_visit=false; timezone=-420; crisp-client%2Fsocket%2Febd7cf0f-b1ee-4a4e-a4ce-8064999c1331=1; ZFSESSID=hslbsj4oi5jcl57g466hksi577; _identity=9ba4164abb6fe28abedc6920bfde91b68479add981e6aa0fc1bade59c3fe28fda%3A2%3A%7Bi%3A0%3Bs%3A9%3A%22_identity%22%3Bi%3A1%3Bs%3A20%3A%22%5B2654139%2Cnull%2C86400%5D%22%3B%7D; last_login=936a33bdb215f75578ef47a19655c714de7c3ca9c29edd47e0e096a332a93320a%3A2%3A%7Bi%3A0%3Bs%3A10%3A%22last_login%22%3Bi%3A1%3Bi%3A1%3B%7D; timezone_key=176YcY1dhXry6zco86w; SERVERID=5dfe92cc422d185f34a1898663840774|1681834051|1681833669; SERVERID=5dfe92cc422d185f34a1898663840774|1681834200|1681833669; is_first_visit=false; sbox-l=en',
    # 'referer': 'https://bigspy.com/iframe/adspy/facebook/?utm_home=1&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsYW4iOiJlbiIsInZlciI6ImJzIiwidGltZXN0YW1wIjoxNjgxODMzNjkyLCJleHBpcmUiOjE2ODIwOTI4OTIsInVzZXJfaWQiOiJTRkJxUVZoWFpnPT0iLCJhcHBuYW1lIjoiQmlnU3B5IiwidXNlcl9uYW1lIjoiZGNyMTY5NjQiLCJzdWJzY3JpcHRpb24iOnsiY29kZSI6ImJpZ3NweV9mcmVlX3RyaWFsIiwiYWRzX3Blcm1pc3Npb24iOnsic2VhcmNoIjoxLCJleGNsdWRlX3NlYXJjaCI6MCwiZmlsdGVyIjoxLCJwYWdlX2xpbWl0IjowLCJxdWVyeV9udW0iOjUsImRvd25sb2FkX251bSI6MH0sIm5ldHdvcmtzIjp7ImZhY2Vib29rIjoxLCJpbnN0YWdyYW0iOjAsInR3aXR0ZXIiOjAsImFkbW9iIjowLCJwaW50ZXJlc3QiOjAsInlhaG9vIjowLCJ5b3V0dWJlIjowLCJ0aWt0b2siOjAsInVuaXR5IjowfSwidHJhY2tfcGVybWlzc2lvbiI6eyJmZWF0dXJlX2FkcyI6MCwicGVvcGxlX2FkcyI6MCwibXlfdHJhY2siOjEsInRyYWNrX251bSI6MjAsInBhZ2VfYW5hbHlzaXMiOjAsInBhZ2VfdHJhY2tfbnVtIjowfSwibW9kdWxlX3Blcm1pc3Npb24iOnsicGFnZV9hbmFseXNpcyI6MCwiZmVhdHVyZV9hZHMiOjB9LCJ0ZWFtX2luZm8iOnsiaWQiOjAsIm5ld190ZWFtX3BvcHVwIjowLCJ0ZWFtX3JlcXVlc3QiOjB9LCJpbmR1c3RyeV9pbmZvIjp7InRvdGFsX2luZHVzdHJ5X2NvdW50IjozLCJyZW1haW5faW5kdXN0cnlfY291bnQiOjMsInBlcm1pc3Npb25fYXBwX3R5cGUiOlsxLDIsM10sImxhc3RfYXBwX3R5cGUiOjB9LCJ1c2VyX3N0YXR1cyI6MSwiaXNfYWRtaW4iOjB9LCJjb21wYW55X2lkIjowLCJlbWFpbCI6Iml4aDUxMTIyQHpzbHN6LmNvbSJ9.iECNN_Isv-9tfyOrbijb6n_fWUmpnil3NVDjFcyraps',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    return json.loads(response.text)

def get_bigspy_ads_detail(token, ad_key):
    url = "https://bigspy.com/ecom/get-ecom-detail?ad_key="+ad_key

    payload={}
    headers = {
    'authority': 'bigspy.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': token,
    'cookie': 'cf_clearance=hqboDiQr4HFISbB7OX2rwLs0KyyWbCdZaZ54C7wVR1E-1681833662-0-250; sbox-l=en; sbox-guid=MTY4MTgzMzY2OXw1MzF8OTk3NjQ4MzE4; _csrf=6ae3d992aa505207ab7f3da555709072a784c931fc0fad7b3af5e7137040362ca%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%227mI9QUtr1gl9GhsZsnuxYcYG-FhR3UhH%22%3B%7D; _uab_collina=168183366964165489189401; anonymous_user_id=4f7a495011f349376caa5989cd3978eb; _trackUserId=G-1681833670000; _ga=GA1.2.650790373.1681833671; _gid=GA1.2.1430911597.1681833671; crisp-client%2Fsession%2Febd7cf0f-b1ee-4a4e-a4ce-8064999c1331=session_4e3077e9-9013-4afa-8e6d-8ebf566cb320; hy_data_2020_id=18795193f87cc0-00ec7cbb30e87d-26031b51-2073600-18795193f882217; hy_data_2020_js_sdk=%7B%22distinct_id%22%3A%2218795193f87cc0-00ec7cbb30e87d-26031b51-2073600-18795193f882217%22%2C%22site_id%22%3A240%2C%22user_company%22%3A87%2C%22props%22%3A%7B%7D%2C%22device_id%22%3A%2218795193f87cc0-00ec7cbb30e87d-26031b51-2073600-18795193f882217%22%7D; sajssdk_2020_cross_new_user=1; zbase_popup_497=4e7780ace6cc2831e91974d1a549cb0307a0a70f421af346676cf7ef2f0509dba%3A2%3A%7Bi%3A0%3Bs%3A15%3A%22zbase_popup_497%22%3Bi%3A1%3Bs%3A10%3A%22isPopup497%22%3B%7D; is_first_visit=false; timezone=-420; crisp-client%2Fsocket%2Febd7cf0f-b1ee-4a4e-a4ce-8064999c1331=1; ZFSESSID=hslbsj4oi5jcl57g466hksi577; _identity=9ba4164abb6fe28abedc6920bfde91b68479add981e6aa0fc1bade59c3fe28fda%3A2%3A%7Bi%3A0%3Bs%3A9%3A%22_identity%22%3Bi%3A1%3Bs%3A20%3A%22%5B2654139%2Cnull%2C86400%5D%22%3B%7D; last_login=936a33bdb215f75578ef47a19655c714de7c3ca9c29edd47e0e096a332a93320a%3A2%3A%7Bi%3A0%3Bs%3A10%3A%22last_login%22%3Bi%3A1%3Bi%3A1%3B%7D; _gat_gtag_UA_121710730_2=1; zbase_popup_497_2654139=2de6cecce254e792506a0bc0f1e0b71e1d6d8260a4463dcbf7dceeffe03586e2a%3A2%3A%7Bi%3A0%3Bs%3A23%3A%22zbase_popup_497_2654139%22%3Bi%3A1%3Bs%3A0%3A%22%22%3B%7D; timezone_key=176YcYYcUfry6zco86w; SERVERID=5dfe92cc422d185f34a1898663840774|1681834727|1681833669; SERVERID=5dfe92cc422d185f34a1898663840774|1681835101|1681833669; is_first_visit=false; sbox-l=en',
    # 'referer': 'https://bigspy.com/iframe/detail?channel=1&id=39654c0079bd934e2e87f7676d41383a&type=3&app_type=&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsYW4iOiJlbiIsInZlciI6ImJzIiwidGltZXN0YW1wIjoxNjgxODM0NzI0LCJleHBpcmUiOjE2ODIwOTM5MjQsInVzZXJfaWQiOiJTRkJxUVZoWFpnPT0iLCJhcHBuYW1lIjoiQmlnU3B5IiwidXNlcl9uYW1lIjoiZGNyMTY5NjQiLCJzdWJzY3JpcHRpb24iOnsiY29kZSI6ImJpZ3NweV9mcmVlX3RyaWFsIiwiYWRzX3Blcm1pc3Npb24iOnsic2VhcmNoIjoxLCJleGNsdWRlX3NlYXJjaCI6MCwiZmlsdGVyIjoxLCJwYWdlX2xpbWl0IjowLCJxdWVyeV9udW0iOjUsImRvd25sb2FkX251bSI6MH0sIm5ldHdvcmtzIjp7ImZhY2Vib29rIjoxLCJpbnN0YWdyYW0iOjAsInR3aXR0ZXIiOjAsImFkbW9iIjowLCJwaW50ZXJlc3QiOjAsInlhaG9vIjowLCJ5b3V0dWJlIjowLCJ0aWt0b2siOjAsInVuaXR5IjowfSwidHJhY2tfcGVybWlzc2lvbiI6eyJmZWF0dXJlX2FkcyI6MCwicGVvcGxlX2FkcyI6MCwibXlfdHJhY2siOjEsInRyYWNrX251bSI6MjAsInBhZ2VfYW5hbHlzaXMiOjAsInBhZ2VfdHJhY2tfbnVtIjowfSwibW9kdWxlX3Blcm1pc3Npb24iOnsicGFnZV9hbmFseXNpcyI6MCwiZmVhdHVyZV9hZHMiOjB9LCJ0ZWFtX2luZm8iOnsiaWQiOjAsIm5ld190ZWFtX3BvcHVwIjowLCJ0ZWFtX3JlcXVlc3QiOjB9LCJpbmR1c3RyeV9pbmZvIjp7InRvdGFsX2luZHVzdHJ5X2NvdW50IjozLCJyZW1haW5faW5kdXN0cnlfY291bnQiOjMsInBlcm1pc3Npb25fYXBwX3R5cGUiOlsxLDIsM10sImxhc3RfYXBwX3R5cGUiOjB9LCJ1c2VyX3N0YXR1cyI6MSwiaXNfYWRtaW4iOjB9LCJjb21wYW55X2lkIjowLCJlbWFpbCI6Iml4aDUxMTIyQHpzbHN6LmNvbSJ9.fRlXfY8C0MV47VPhBRHCLq5eL1jlV-GonhAWHJp4Ehw',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return json.loads(response.text)

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

    response = requests.request("GET", url, headers=headers, data=payload)
    return json.loads(response.text)

def get_bigspy_henull_tiktok_ads_list(base_domain, page, token, cookie):
    base_url = "https://"+base_domain
    url = base_url+"/ecom/get-ecom-ads?favorite_app_flag=0&ecom_category=&search_type=1&platform=43&category=0&os=0&ads_promote_type=0&geo=VNM&game_play=0&game_style=&type=2&page="+ str(page) +"&industry=3&language=&keyword=&sort_field=first_seen&region=&original_flag=0&is_preorder=0&theme=&text_md5=&ads_size=&ads_format=&exclude_keyword=&cod_flag=0&cta_type=0&new_ads_flag=0&like_begin=1000&like_end=&comment_begin=&comment_end=&share_begin=&share_end=&position=0&is_hide_advertiser=0&advertiser_key=&dynamic=0&shopping=0&duplicate=0&software_types=&ecom_types=&social_account=&modules=ecomad&page_id=&landing_type=0&is_first=0&page_load_more=1&source_app="
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

    response = requests.request("GET", url, headers=headers, data=payload)

    return json.loads(response.text)


def get_bigspy_henull_ads_detail(base_domain, ad_key, token, cookie):
    base_url = "https://"+base_domain
    url = base_url+"/ecom/get-ecom-detail?ad_key="+ad_key

    payload={}
    headers = {
    'authority': base_domain,
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': token,
    'cookie': cookie,
    # 'referer': 'https://l9gr5r2r.realnull.com/iframe/detail?channel=1&id=39654c0079bd934e2e87f7676d41383a&type=3&app_type=&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsYW4iOiJlbiIsInZlciI6ImJzIiwidGltZXN0YW1wIjoxNjgxODM0NzI0LCJleHBpcmUiOjE2ODIwOTM5MjQsInVzZXJfaWQiOiJTRkJxUVZoWFpnPT0iLCJhcHBuYW1lIjoiQmlnU3B5IiwidXNlcl9uYW1lIjoiZGNyMTY5NjQiLCJzdWJzY3JpcHRpb24iOnsiY29kZSI6ImJpZ3NweV9mcmVlX3RyaWFsIiwiYWRzX3Blcm1pc3Npb24iOnsic2VhcmNoIjoxLCJleGNsdWRlX3NlYXJjaCI6MCwiZmlsdGVyIjoxLCJwYWdlX2xpbWl0IjowLCJxdWVyeV9udW0iOjUsImRvd25sb2FkX251bSI6MH0sIm5ldHdvcmtzIjp7ImZhY2Vib29rIjoxLCJpbnN0YWdyYW0iOjAsInR3aXR0ZXIiOjAsImFkbW9iIjowLCJwaW50ZXJlc3QiOjAsInlhaG9vIjowLCJ5b3V0dWJlIjowLCJ0aWt0b2siOjAsInVuaXR5IjowfSwidHJhY2tfcGVybWlzc2lvbiI6eyJmZWF0dXJlX2FkcyI6MCwicGVvcGxlX2FkcyI6MCwibXlfdHJhY2siOjEsInRyYWNrX251bSI6MjAsInBhZ2VfYW5hbHlzaXMiOjAsInBhZ2VfdHJhY2tfbnVtIjowfSwibW9kdWxlX3Blcm1pc3Npb24iOnsicGFnZV9hbmFseXNpcyI6MCwiZmVhdHVyZV9hZHMiOjB9LCJ0ZWFtX2luZm8iOnsiaWQiOjAsIm5ld190ZWFtX3BvcHVwIjowLCJ0ZWFtX3JlcXVlc3QiOjB9LCJpbmR1c3RyeV9pbmZvIjp7InRvdGFsX2luZHVzdHJ5X2NvdW50IjozLCJyZW1haW5faW5kdXN0cnlfY291bnQiOjMsInBlcm1pc3Npb25fYXBwX3R5cGUiOlsxLDIsM10sImxhc3RfYXBwX3R5cGUiOjB9LCJ1c2VyX3N0YXR1cyI6MSwiaXNfYWRtaW4iOjB9LCJjb21wYW55X2lkIjowLCJlbWFpbCI6Iml4aDUxMTIyQHpzbHN6LmNvbSJ9.fRlXfY8C0MV47VPhBRHCLq5eL1jlV-GonhAWHJp4Ehw',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return json.loads(response.text)

def get_shoplus_ads_list(page, token, cookie):
    url = "https://www.shoplus.net/api/v1/tikmeta/portal/ads/search?cursor="+ str(page) +"&region=VN&keyword_type=ALL&sort=1&play_count_start=100000"

    payload={}
    headers = {
        'authority': 'www.shoplus.net',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': token,
        'client-ver': 'null',
        'cookie': cookie,
        'device-id': '156929242966862pglxzgbwqdhyavmneko',
        'eagleeye-pappname': 'cjqlxc9zwk@45505ea362bfd04',
        'eagleeye-sessionid': '6klv7g58pmtbakvtp66stO5x287w',
        'eagleeye-traceid': 'dcb98d9916820076503641012bfd04',
        # 'referer': 'https://www.shoplus.net/discovery/ads',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'session-id': '31388914104729toqgcfzhgxpbskylrma',
        'source-url': 'https://www.shoplus.net/home',
        'system-id': '14',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'user-id': '176171',
        'x-language': 'vi',
        'x-requested-with': 'XMLHttpRequest'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return json.loads(response.text)

def get_shoplus_ads_detail(ad_key, author_id, video_id, last_time, token, cookie):
    url = "https://www.shoplus.net/api/v1/tikmeta/portal/ads/detail?ad_id="+ad_key+"&last_time="+last_time+"&author_id="+author_id+"&video_id="+video_id

    payload = {}
    headers = {
        'authority': 'www.shoplus.net',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': token,
        'client-ver': 'null',
        'cookie': cookie,
        'device-id': '156929242966862pglxzgbwqdhyavmneko',
        'eagleeye-pappname': 'cjqlxc9zwk@45505ea362bfd04',
        'eagleeye-sessionid': 'vmlUXgbmqttsp2imyx6yb8q8m0CO',
        'eagleeye-traceid': '34f9278d16820959970731001bfd04',
        # 'referer': 'https://www.shoplus.net/ads/detail?adId=1758363763619873&lastTime=2023-04-21&authorId=7079970251038983169&videoId=7202218226128915713',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'session-id': '31388914104729toqgcfzhgxpbskylrma',
        # 'source-url': 'https://www.shoplus.net/ads/detail?adId=1758363763619873&lastTime=2023-04-21&authorId=7079970251038983169&videoId=7202218226128915713',
        'system-id': '14',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'user-id': '176171',
        'x-language': 'vi',
        'x-requested-with': 'XMLHttpRequest'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return json.loads(response.text)
