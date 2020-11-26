import boto3

# dynamodb init connection
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Account')

# get the account name function for the skill, used to then query the account
# name for a prediction to be formed
def format_account_name(slots):
    slot_names_list = ["CharacterOne", "CharacterTwo", "CharacterThree", "CharacterFour",
                       "CharacterFive", "CharacterSix", "CharacterSeven",
                       "CharacterEight", "CharacterNine", "CharacterTen",
                       "CharacterEleven", "CharacterTwelve", "CharacterThirteen",
                       "CharacterFourteen", "CharacterFifteen", "CharacterSixteen"]
    last_char = ["why", "you", "ess", "arr", "enn", "emm", "ell", "eff"]
    first_char = ["zed", "zee", "vee", "tea", "queue", "pee", "ohh", "kay", "jay",
                  "heitch", "gee", "ee", "dee", "cee", "bee"]
    account_name_list = []
    for name in slot_names_list:
        if 'value' in slots[name]:
            value = slots[name]['value'].lower()
            if '.' in value:
                value = value.replace(".", "")
            if len(value) > 1:
                if any(char == value for char in last_char):
                    account_name_list.append(value[2])
                elif any(char == value for char in first_char):
                    account_name_list.append(value[0])
                else:
                    converted_value = convert_string(value)
                    if converted_value is None:
                        account_name_list.append(value[0])
                    else:
                        account_name_list.append(converted_value)
            else:
                account_name_list.append(value)
                
    account_name = ''.join(account_name_list)
    if len(account_name) < 3 or len(account_name) > 16:
        return "Account Length Error"
    else:
        return account_name


# switch statement converting passed strings to appropriate values
def convert_string(i):
    switcher = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
        'zero': 0,
        'space': ' ',
        'ae': 'a',
        'ayy': 'i',
        'eye': 'i',
        'ex': 'x',
        'double you': 'w'
    }
    if type(switcher.get(i)) is int:
        return str(switcher.get(i))
    else:
        return switcher.get(i)

# split the passed name into characters for Alexa to spell out to the user
def split_name(name):
    name_char_list = list(name)
    split_char_name = []
    for i, char in enumerate(name_char_list):
        if i == len(name_char_list):
            if char == " ":
                split_char_name.append("space.")
            else:
                split_char_name.append(char + ".")
        else:
            if char == " ":
                split_char_name.append("space. ")
            else:
                split_char_name.append(char + ". ")
    
    split_char_string = "".join(split_char_name)
    return split_char_string


# check if the passed database entry exists, if not then returns None
def in_database(ask_id):
    db_item = table.get_item(Key={'AccountID': ask_id})
    if 'Item' in db_item:
        item = db_item['Item']
        return item
    else:
        return None


# parse the unique alexa id and return the alphanumeric id associated with a user
def parse_id(ask_id):
    split_id = ask_id.split(".", 4)
    unique_id = split_id[3]
    return unique_id
    