from babel import Locale
from import_export import resources
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

def to_number(num):
    number = 0
    try:
        number = int(num)
    except:
        if num != None:
            strchar = num[-1]
            strnum = num[:-1]
            number = float(strnum)
            if strchar == "K":
                number *= 1000
            elif strchar == "M":
                number *= 1000000
            number = round(number)
    return number
    
def country_to_str(item) -> str:
    countries = []
    locale = Locale('vi')  # Tạo đối tượng Locale cho ngôn ngữ tiếng Việt
    for i in range(len(item['countries'])):
        try:
            countries.append(locale.territories[item['countries'][i]])
        except KeyError:
            try:
                countries.append(locale.territories[item['countries'][i][:2]])
            except KeyError:
                countries.append(item['countries'][i])
    return ", ".join(countries)

def clean_str(v):
    if type(v) == str:
      v = ILLEGAL_CHARACTERS_RE.sub('', v)
    return v

if __name__ == "__main__":
    # item = {
    #     "countries": ["USA", "IND"]
    # }
    # print(country_to_str(item))
    print(clean_str("mua TÚI CHÉO TAIJANG"))
