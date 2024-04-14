class DonateStruc():

    def __init__(self, id, name,info,transferDetails,appointment,url):
        self.id = id
        self.name = name
        self.info = info
        self.transferDetails = transferDetails
        self.appointment = appointment
        self.link = url


donate_list = [

DonateStruc(0, "БФ Гуркіт","Рахунок у гривнях (МоноБанк)","Картка: 5375 4114 3225 3479","На армію","https://hurkit.org/donate"),
DonateStruc(0, "БФ Гуркіт","Рахунок у гривнях (ПриватБанк)","Картка: 5169 3351 0084 3610","На армію","https://hurkit.org/donate"),
DonateStruc(0, "БФ Гуркіт","Благодійна організація «Благодійний фонд «Гуркіт»","ЄДРПОУ: 44823498","На армію","https://hurkit.org/donate"),
DonateStruc(0, "БФ Гуркіт","PayPal","funds@hurkit.org","На армію","https://hurkit.org/donate"),
DonateStruc(0, "БФ Гуркіт","Рахунок в доларах","IBAN: UA163052990000026007046816146","На армію","https://hurkit.org/donate"),
DonateStruc(0, "БФ Гуркіт","Рахунок в євро","IBAN: UA393052990000026006046814699","На армію","https://hurkit.org/donate"),
DonateStruc(1, "Благодійний фонд Рій","SWIFT  в долларах (USD)","IBAN: UA863052990000026004041039705","На армію","https://www.riyukraine.com/payments"),
DonateStruc(1, "Благодійний фонд Рій","SWIFT в євро (EUR)","IBAN: UA803052990000026002041020578","На армію","https://www.riyukraine.com/payments"),
DonateStruc(1, "Благодійний фонд Рій","Поповнення карти в Приват","ЄДРПОУ 44855404","На армію","https://www.riyukraine.com/payments"),
DonateStruc(1, "Благодійний фонд Рій","Поповнення карти в моно","ЄДРПОУ 21133352","На армію","https://www.riyukraine.com/payments"),
DonateStruc(1, "Благодійний фонд Рій","Поповнення PayPal","riyukraine@gmail.com","На армію","https://www.riyukraine.com/payments"),
DonateStruc(2, "БО 'БЛАГОДІЙНИЙ ФОНД ПОБАЧ ПЕРЕМОГУ'","ГРИВНЯ","IBAN: UA063052990000026004036234504","Гуманітарна","https://www.see-the-victory.com/requisites"),
DonateStruc(2, "БО 'БЛАГОДІЙНИЙ ФОНД ПОБАЧ ПЕРЕМОГУ'","ЄВРО","IBAN: UA043052990000026005006229496","Гуманітарна","https://www.see-the-victory.com/requisites"),
DonateStruc(2, "БО 'БЛАГОДІЙНИЙ ФОНД ПОБАЧ ПЕРЕМОГУ'","ДОЛАР","IBAN: UA303052990000026005036238015","Гуманітарна","https://www.see-the-victory.com/requisites"),
DonateStruc(2, "БО 'БЛАГОДІЙНИЙ ФОНД ПОБАЧ ПЕРЕМОГУ'","PAYPAL","foundation@zir.org.ua","Гуманітарна","https://www.see-the-victory.com/requisites"),
DonateStruc(3, "БФ 'RAZOM'","BTC","wallet: bc1qyz4pffdh04xhxyldlv6mktvkw3jxcehc707dr7","Гуманітарна","https://www.razomforukraine.org/ua/donate-ua/"),
DonateStruc(3, "БФ 'RAZOM'","ETH","wallet: 0xA4166BC4Be559b762B346CB4AAad3b051E584E39","Гуманітарна","https://www.razomforukraine.org/ua/donate-ua/"),
DonateStruc(4, "соломʼянські котики","гривня","IBAN: UA283052990000026003045019432","Гуманітарна","https://kittysoloma.org/#how-to-help"),
DonateStruc(4, "соломʼянські котики","долар","IBAN: UA593052990000026002025031282","Гуманітарна","https://kittysoloma.org/#how-to-help"),
DonateStruc(4, "соломʼянські котики","Приватбанк","5169 3351 0016 4686","Гуманітарна","https://kittysoloma.org/#how-to-help"),
DonateStruc(4, "соломʼянські котики","PayPal","ae.dexter26@gmail.com","Гуманітарна","https://kittysoloma.org/#how-to-help"),
DonateStruc(4, "соломʼянські котики","Ethereum","0x1f4c09CE996b14d361393e73Bd45C001469e5109","Гуманітарна","https://kittysoloma.org/#how-to-help"),
DonateStruc(4, "соломʼянські котики","Bitcoin","bc1q0rg3pfheqzfpe6zzzj7gzx7xr35y9yf3neujp7","Гуманітарна","https://kittysoloma.org/#how-to-help"),
DonateStruc(4, "соломʼянські котики","USDT (Tether ERC20)","0x1f4c09CE996b14d361393e73Bd45C001469e5109","Гуманітарна","https://kittysoloma.org/#how-to-help")
]

def get_donation_structs_by_group(group):
    structs=[]
    for item in donate_list:
        if item.appointment == group:
            structs.append(item)
    return structs

def get_donate_struct_by_id(id):
    return list(filter(lambda x: x.id == id, donate_list))


def get_Unique_Name():
    unique_names=[]
    for item in donate_list:
        if item.name not in unique_names:
            unique_names.append(item.name)
    return unique_names


def get_Unique_Appointment():
    unique=[]
    for item in donate_list:
        if item.appointment not in unique:
            unique.append(item.appointment)
    return unique


def get_Donate_info(name):
    link = ""
    req=""
    for i in donate_list:

        if name == i.name:
            req+=f"{i.info}\n{i.transferDetails}\n\n"
            if link == "":
                link = i.link

    result = f"""
Назва::{name}
            
Реквізити::
{req}
            
Посилання::
{link}
"""

    print(result)


def get_names_in_ids(group):
    tmp=[]
    for i in donate_list:
        if group == i.appointment:
            tmp.append(i.id)
    return set(tmp)


for i in get_Unique_Name():
    print(i)

print()
for i in get_Unique_Appointment():
    print(i)

# get_Donate_info("БФ Гуркіт")

